#!/bin/python
import argparse
from copy import copy
from lxml import etree
from collections import defaultdict
from morphdecompose import morph_dict

def ctm_to_index(ctm_path, morph_dict_path=None, output=None):
    index = dict()
    transcript = []
    token_indexes = defaultdict(list)

    if morph_dict_path:
        morphs = morph_dict(morph_dict_path)

    with open(ctm_path, 'r') as f:
        for line in f.readlines():
            if len(line.split()) == 6:
                filename, channel, start, raw_duration, raw_token, posterior = line.split()

                if morph_dict_path:
                    tokens = morphs[raw_token.lower()]
                else:
                    tokens = [raw_token]

                for token_index, token in enumerate(tokens):
                    duration = float(raw_duration)/len(tokens)
                    start = float(start) + token_index * duration

                    entry = {
                        "filename": filename,
                        "channel": int(channel),
                        "start": start,
                        "duration": duration,
                        "token": token.lower(),
                        "posterior": float(posterior),
                    }
                    transcript_index = len(transcript)
                    transcript.append(entry)
                    token_indexes[entry["token"]].append(transcript_index)
            else:
                raise Exception("Unexpected formatting in CTM file")

    if output:
        with open(output, 'w') as f:
            for entry in transcript:
                f.write("{filename} {channel} {start:0.2f} {duration:0.3f} "
                    "{token} {posterior:0.4f}\n".format(**entry))


    index["transcript"] = transcript
    index["token_indexes"] = token_indexes

    return index


"""Query an index with a list of key words, returns a dict of results"""
def query(index, queries_xml, morph_dict_path=None):
    tree = etree.parse(queries_xml)
    querylist = tree.getroot()
    kws_results = []

    if morph_dict_path:
        morphs = morph_dict(morph_dict_path)

    for kw in querylist:
        kwid = kw.values()[0]
        kwtext = kw.getchildren()[0].text
        kw_search = {"kwid": kwid, "hits": []}
        phrase_split = kwtext.lower().split()
        tokens = []
        if morph_dict_path:
            morphs = morph_dict(morph_dict_path)
            for token in phrase_split:
                if token not in morphs:
                    print(token)  #TODO, should morphs have to come from the kws dict?
                tokens.extend(morphs.get(token, [token]))
        else:
            tokens = phrase_split

        hits = []

        # Follow the find sequence of tokens that match the phrase
        start_entry_indexes = index["token_indexes"][tokens[0]]

        for i in start_entry_indexes:
            token_count, entry_count = 1, 1
            start_entry = index["transcript"][i]
            entry = start_entry
            duration = entry["duration"]
            posterior = entry["posterior"]
            last_end_time = start_entry["start"] + start_entry["duration"]

            while True:

                if token_count == len(tokens):
                    # Success! Found the final token of the phrase within
                    hit = {
                        "filename": start_entry["filename"],
                        "channel": start_entry["channel"],
                        "start": start_entry["start"],
                        "duration": duration,
                        "token": kwtext,
                        "posterior": posterior,
                        "decision": True  # Eval system will choose threshold.
                    }
                    hits.append(hit)
                    break

                i += 1
                entry = index["transcript"][i]
                if entry["token"] == tokens[token_count] and entry["filename"] == start_entry["filename"]:
                    curr_time = entry["start"]
                    if curr_time - last_end_time <= 0.5:
                        token_count += 1
                        duration += entry["duration"]
                        posterior = (posterior*(token_count-1) + entry['posterior'])/token_count
                        last_end_time = entry["start"] + entry["duration"]
                        continue
                break

        kw_search["hits"] = hits
        kws_results.append(kw_search)

    return kws_results


def kws_output(kws_results, output_path):

    # create XML
    kwslist = etree.Element('kwslist')
    kwslist.set("kwlist_filename", "IARPA-babel202b-v1.0d_conv-dev.kwlist.xml")
    kwslist.set("language", "swahili")
    kwslist.set("system_id", "")

    for kw_search in kws_results:
        detected_kwlist = etree.Element("detected_kwlist")
        detected_kwlist.set("kwid", kw_search["kwid"])
        detected_kwlist.set("oov_count", "0")
        detected_kwlist.set("search_time", "0.0")

        for hit in kw_search["hits"]:
            kw = etree.Element("kw")
            kw.set("file", hit["filename"])
            kw.set("channel", str(hit["channel"]))
            kw.set("tbeg", str(hit["start"]))
            kw.set("dur", str(hit["duration"]))
            kw.set("score", str(hit["posterior"]))
            decision = "YES" if hit["decision"] else "NO"
            kw.set("decision", decision)
            detected_kwlist.append(kw)

        if not kw_search["hits"]:
            # Set string as element content to force separate open and close tags
            detected_kwlist.text = "\n"

        kwslist.append(detected_kwlist)

    tree = etree.ElementTree(kwslist)
    tree.write(output_path, pretty_print=True, xml_declaration=False)
    return tree


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract a CTM file')
    parser.add_argument('ctm', type=str, help='Reference CTM Name')
    # parser.add_argument('--output', type=str, # help='Optinal output file')
    args = parser.parse_args()
    index = ctm_to_index(args.ctm)
    kws_results = query(index, 'lib/kws/queries.xml')
    # kws_output(kws_results, args.ctm)
