# Jordan Burgess
# MLSALT5 CW

# Directory Layout
lib/               <- Practical provided files such as CTMs (1best lists from an ASR) and the KSR queries
mylib/             <- A few things like modified CTMs (not really used)
output/            <- Results from KWS
outputcombined/    <- Combinations of results from KWS
reference_scoring/ <- Provided evaluations of known systems
scoring/           <- Evaluations of results from KWS
scoringcombined/   <- Evaluations of combinations results from KWS
scripts/           <- Scripts to evaluate results

combined_kws.py    <- Merge the results of separate KWS systems
helpers.py         <- Misc python helpers
keyword_search.py  <- MAIN FILE. Has functions to turn ctm to an index, search an index, save the results.
morph_decompose.py <- Build a dictionary morphological decompositions
normalise_kws.py   <- Given a KWS output, renormalise the scores.
test.py            <- Sandbox to run scripts from

