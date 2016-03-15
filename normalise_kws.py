#!/bin/python
import argparse
from lxml import etree

""" Given a KWS output XML, renormalise the scores for each hit """
def normalise_kws_output(kws_path, output_path, gamma):
    tree = etree.parse(kws_path)
    kwslist = tree.getroot()

    for detected_kwlist in kwslist:
        sum_of_scores = sum([float(hit.get("score"))**gamma for hit in detected_kwlist])
        for hit in detected_kwlist:
            hit.set("score", str((float(hit.get("score"))**gamma)/sum_of_scores))

    tree.write(output_path, pretty_print=True, xml_declaration=False)
    return tree

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Normalise scores of a KWS output')
    parser.add_argument('kws_path', type=str, help='Source KWS results')
    parser.add_argument('output_path', type=str, help='Output path')
    parser.add_argument('gamma', type=str, default=1, help='Parameter to exponentiate scores (default=1)')
    args = parser.parse_args()
    tree = normalise_kws_output(args.kws_path, args.output_path, args.gamms)
