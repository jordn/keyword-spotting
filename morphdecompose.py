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

def decompose_ctm(ctm_path, morphs, decomposed_ctm_path=None):
    index = []
    with open(ctm_path, 'r') as f:
        for line in f.readlines():
            line_split = line.split()
            assert(len(line_split) == 6)
            filename, channel, start, duration, token, posterior = line.split()
            token_morphs = morphs[token.lower()]
            for i, morph in enumerate(token_morphs):
                morph_duration = float(duration)/len(token_morphs)
                entry = {"filename": filename,
                        "channel": int(channel),
                        "start": float(start) + i * morph_duration,
                        "duration": morph_duration,
                        "token": morph.lower(),
                        "posterior": float(posterior), #TODO, should this change?
                }
                index.append(entry)

    if decomposed_ctm_path:
        with open(decomposed_ctm_path, 'w') as f:
            for entry in index:
                f.write("{filename} {channel} {start:0.2f} {duration:0.3f} "
                    "{token} {posterior:0.4f}\n".format(**entry))

    return index

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Morphologically decompose a CTM file')
    parser.add_argument('ctm', type=str, help='Reference CTM Name')
    parser.add_argument('--output', type=str, help='Optional output file')
    args = parser.parse_args()
    morphs = morph_dict('lib/dicts/morph.dct')
    index = decompose_ctm(args.ctm, morphs, args.output)
    # kws_output(kws_results, args.ctm)
    # kws_output(kws_results, args.ctm)
