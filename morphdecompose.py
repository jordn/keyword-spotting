#!/bin/python
import argparse
from lxml import etree


def morph_dict(morph_path):
    morphs = dict()
    with open(morph_path, 'r') as f:
        for line in f.readlines():
            line_split = line.split()
            morphs[line_split[0].lower()] = line_split[1:]

    return morphs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Morphologically decompose a CTM file')
    parser.add_argument('ctm', type=str, help='Reference CTM Name')
    parser.add_argument('--output', type=str, help='Optional output file')
    args = parser.parse_args()
    morphs = morph_dict('lib/dicts/morph.dct')
