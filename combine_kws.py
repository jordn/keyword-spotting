#!/bin/python
import argparse
import copy

from lxml import etree

# def load_kws_results(kws_path):
#     tree = etree.parse(kws_path)
#     kwslist = tree.getroot()


def kw_overlap(kw1, kw2):
    """ Returns true if the two kw hits are pointing at the same reference """
    if kw1.get("file") == kw2.get("file"):
        start1 = float(kw1.get("tbeg"))
        end1 = start1 + float(kw1.get("tbeg"))
        start2 = float(kw2.get("tbeg"))
        end2 = start2 + float(kw2.get("tbeg"))
        # Check for any overlap
        if end1 >= start2 and end2 >= start1:
            return True
    return False


def combine_kws(kws1_path, kws2_path, output_path):
    """ Given a KWS output XML, renormalise the scores for each hit """

    tree1 = etree.parse(kws1_path)
    kwslist1 = tree1.getroot()

    tree2 = etree.parse(kws2_path)
    kwslist2 = tree2.getroot()

    for detected_kwlist1 in kwslist1:

        # Find the same kwid in second list (sets may not be identical)
        kwid = detected_kwlist1.get("kwid")
        detected_kwlists2 = kwslist2.xpath("//detected_kwlist[@kwid='{}']".format(kwid))

        assert len(detected_kwlists2) <= 1

        if len(detected_kwlists2) == 1:
            detected_kwlist2 = detected_kwlists2[0]

            for kw1 in detected_kwlist1:
                for kw2 in detected_kwlist2:
                    if kw_overlap(kw1, kw2):
                        # Return the merge KW (use times from kw1, take sum of scores)
                        # TODO, explore whether max or sum is best.
                        kw1.set("score", str(
                            # max(float(kw1.get("score")), float(kw2.get("score")))
                            float(kw1.get("score")) +  float(kw2.get("score"))
                        ))
                        detected_kwlist2.remove(kw2)
                        break

            # Add any leftover kw2s that didn't overlap
            for kw2 in detected_kwlist2:
                detected_kwlist1.append(kw2)

            # detected_kwlist2 now empty. Remove so we can find any leftovers.
            kwslist2.remove(detected_kwlist2)


    # Add any remaining detected_kwlists to kwlist1
    if len(kwslist2) > 0:
        for detected_kwlist2 in kwslist2:
            kwslist1.append(detected_kwlist2)

    tree1.write(output_path, pretty_print=True, xml_declaration=False)
    return tree1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine KWS outputs')
    parser.add_argument('kws1_path', type=str, help='Source 1 KWS results')
    parser.add_argument('kws2_path', type=str, help='Source 2 KWS results')
    parser.add_argument('output_path', type=str, help='Output path')
    args = parser.parse_args()
    tree = combine_kws(args.kws1_path, args.kws2_path, args.output_path)
