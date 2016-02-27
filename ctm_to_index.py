#!/bin/python
import argparse
from copy import copy
from lxml import etree
# from collections import deque
# import numpy as np

def ctm_to_index(ctm_path, output=None):
    index = []
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
                index.append(entry)
            else:
                raise Exception("Unexpected formatting in CTM file")
    return index


"""Query an index with a list of key words, returns a dict of results"""
def query(index, queries_xml):
    tree = etree.parse(queries_xml)
    querylist = tree.getroot()
    kws_results = []

    for kw in querylist:
        kwid = kw.values()[0]
        kwtext = kw.getchildren()[0].text

        kw_search = {"kwid": kwid, "hits": []}
        threshold = 1.0
        tokens = kwtext.split()

        if len(tokens) == 1:
            hits = filter(lambda entry: entry['token'].lower() == kwtext.lower(), index)
        else:
            # Search through to find sequence of tokens that make a phrase
            num_tokens = len(tokens)
            hits = []
            i, end_time, duration, posterior = 0, 0, 0, 0
            for entry in index:
                if entry['token'].lower() == tokens[i] and (end_time == 0 or entry['start'] <= end_time + 0.5):
                    if i == 0:
                        start = entry['start']
                    i += 1;
                    end_time = entry['start'] + entry['duration']
                    duration += entry['duration'] #test
                    posterior = (posterior*(i-1) + entry['posterior'])/i # Mean of posteriors seen TODO change?
                    if i == num_tokens:
                       # Made it to the end of the phrase.
                        hit = {
                            "filename": entry['filename'],
                            "channel": entry['channel'],
                            "start": float(start),
                            "duration": duration,
                            "token": kwtext,
                            "posterior": float(posterior),
                        }
                        hits.append(hit)
                        i, end_time, duration = 0, 0, 0
                else:
                    i, end_time, duration = 0, 0, 0

        for hit in hits:
            if hit["posterior"] >= threshold:
                hit["decision"] = True
            else:
                hit["decision"] = False
            kw_search["hits"].append(hit)

        kws_results.append(kw_search)

    return kws_results


def kws_output(kws_results, output="output/reference2.xml"):
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
    tree.write(output, pretty_print=True, xml_declaration=False)
    return tree


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract a CTM file')
    parser.add_argument('ctm', type=str,
        help='Path to reference CTM')
    # parser.add_argument('--output', type=str,
        # help='Optinal output file')
    args = parser.parse_args()
    index = ctm_to_index(args.ctm)
    kws_results = query(index, 'lib/kws/queries.xml')
    kws_output(kws_results)
