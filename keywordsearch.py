#!/bin/python
import argparse
from copy import copy
from lxml import etree
from collections import defaultdict
# from collections import deque
# import numpy as np


def ctm_to_index(ctm_name, output=None):
    index = dict()
    transcript = []
    token_indexes = defaultdict(list)
    ctm_path = 'lib/ctms/' + ctm_name + '.ctm'
    with open(ctm_path, 'r') as f:
        for line in f.readlines():
            if len(line.split()) == 6:
                filename, channel, start, duration, token, posterior = line.split()
                entry = {"filename": filename,
                        "channel": int(channel),
                        "start": float(start),
                        "duration": float(duration),
                        "token": token.lower(),
                        "posterior": float(posterior),
                }
                i = len(transcript)
                transcript.append(entry)
                token_indexes[entry["token"]].append(i)
            else:
                raise Exception("Unexpected formatting in CTM file")

    index["transcript"] = transcript
    index["token_indexes"] = token_indexes

    # # Add key to each entry with the next token to speed up phrase search
    # for i in range(len(transcript)-2, 0, -1):
    #     entry = transcript[i]
    #     if entry["filename"] == transcript[i+1]["filename"]:
    #         entry["next"] = transcript[i+1]

    return index


"""Query an index with a list of key words, returns a dict of results"""
def query(index, queries_xml, morphs=None):
    tree = etree.parse(queries_xml)
    querylist = tree.getroot()
    kws_results = []

    for kw in querylist:
        kwid = kw.values()[0]
        kwtext = kw.getchildren()[0].text
        kw_search = {"kwid": kwid, "hits": []}
        threshold = 1.0
        phrase_split = kwtext.lower().split()
        tokens = []
        if morphs:
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
            duration = start_entry["duration"]
            posterior = start_entry["posterior"]

            while (duration <= 0.5):
                if token_count == len(tokens):
                    # Success! Found the final token of the phrase within
                    hit = {
                        "filename": start_entry["filename"],
                        "channel": start_entry["channel"],
                        "start": start_entry["start"],
                        "duration": duration,
                        "token": kwtext,
                        "posterior": posterior,
                    }
                    hits.append(hit)
                    break

                i += 1
                entry = index["transcript"][i+1]

                if start_entry["filename"] != entry["filename"]:
                    break

                entry_count += 1
                duration += entry["duration"]
                posterior = (posterior * (entry_count-1) + entry['posterior'])/entry_count  # Mean of posteriors seen TODO change?

                if entry["token"] == tokens[token_count]:
                    token_count += 1

        for hit in hits:
            if hit["posterior"] >= threshold:
                hit["decision"] = True
            else:
                hit["decision"] = False
            kw_search["hits"].append(hit)

        kws_results.append(kw_search)

    return kws_results


def kws_output(kws_results, output_name):

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
            # Set empty string as element content to force open and close tags
            detected_kwlist.text = "    "

        kwslist.append(detected_kwlist)

    tree = etree.ElementTree(kwslist)
    output_path = "output/" + output_name + ".xml"
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
