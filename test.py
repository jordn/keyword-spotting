from keywordsearch import ctm_to_index, query, kws_output
from normalise_kws import normalise_kws_output
from morphdecompose import morph_dict
from combine_kws import combine_kws

from timeit import Timer
import time
import datetime
from helpers import subprocess_call

# t = Timer('[x for x in l[::-1]]', 'l = list(range(100000))')
# t.timeit(number=1000)
# start = time.time()
# old_index = old_ctm_to_index('reference')
# end = time.time()
# print(end - start)
# start = time.time()
# old_kws_results = old_query(old_index, 'lib/kws/queries.xml')
# end = time.time()
# print(end - start)

# index = ctm_to_index('lib/ctms/reference.ctm')
# kws_results = query(index, 'lib/kws/queries.xml')
# kws_output(kws_results, 'reference')
# subprocess_call("rm -rf scoring/reference")
# subprocess_call("scripts/score.sh output/reference.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring all")

# index = ctm_to_index('lib/ctms/decode.ctm')
# kws_results = query(index, 'lib/kws/queries.xml')
# kws_output(kws_results, 'decode')
# subprocess_call("rm -rf scoring/decode")
# subprocess_call("scripts/score.sh output/decode.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode.xml scoring all")



# # No Score normalisation
# index = ctm_to_index('lib/ctms/decode.ctm', 'lib/dicts/morph.dct', 'mylib/ctms/decode-decomposed.ctm')
# kws_results = query(index, 'lib/kws/queries.xml', 'lib/dicts/morph.kwslist.dct')
# kws_output(kws_results, 'decode-decomposed')
# subprocess_call("rm -rf scoring/decode-decomposed")
# subprocess_call("scripts/score.sh output/decode-decomposed.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-decomposed.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-decomposed.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-decomposed.xml scoring oov")

# index = ctm_to_index('lib/ctms/decode-morph.ctm')
# kws_results = query(index, 'lib/kws/queries.xml', 'lib/dicts/morph.kwslist.dct')
# kws_output(kws_results, 'decode-morph')
# subprocess_call("rm -rf scoring/decode-morph")
# subprocess_call("scripts/score.sh output/decode-morph.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-morph.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-morph.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-morph.xml scoring oov")

# ##########################################################################################
# # Score normalisation (gamma = 1)
############################################################################################
# index = ctm_to_index('lib/ctms/reference.ctm')
# kws_results = query(index, 'lib/kws/queries.xml')
# kws_output(kws_results, 'output/reference.xml')
# normalise_kws_output('output/reference.xml', 'output/reference-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/reference-gamma1")
# subprocess_call("scripts/score.sh output/reference-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/reference-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/reference-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/reference-gamma1.xml scoring oov")

# index = ctm_to_index('lib/ctms/decode.ctm')
# kws_results = query(index, 'lib/kws/queries.xml')
# kws_output(kws_results, 'output/decode.xml')
# normalise_kws_output('output/decode.xml', 'output/decode-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/decode-gamma1")
# subprocess_call("scripts/score.sh output/decode-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-gamma1.xml scoring oov")

# index = ctm_to_index('lib/ctms/decode.ctm', 'lib/dicts/morph.dct', 'mylib/ctms/decode-decomposed.ctm')
# kws_results = query(index, 'lib/kws/queries.xml', 'lib/dicts/morph.kwslist.dct')
# kws_output(kws_results, 'output/decode-decomposed.xml')
# normalise_kws_output('output/decode-decomposed.xml', 'output/decode-decomposed-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/decode-decomposed-gamma1")
# subprocess_call("scripts/score.sh output/decode-decomposed-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-decomposed-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-decomposed-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-decomposed-gamma1.xml scoring oov")

# index = ctm_to_index('lib/ctms/decode-morph.ctm')
# kws_results = query(index, 'lib/kws/queries.xml', 'lib/dicts/morph.kwslist.dct')
# kws_output(kws_results, 'output/decode-morph.xml')
# normalise_kws_output('output/decode-morph.xml', 'output/decode-morph-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/decode-morph-gamma1")
# subprocess_call("scripts/score.sh output/decode-morph-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-gamma1.xml scoring oov")

#############################################################################
# IBM Systems
#############################################################################

# subprocess_call("rm -rf scoring/word")
# subprocess_call("scripts/score.sh lib/kws/word.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/word.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/word.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/word.xml scoring oov")

# subprocess_call("rm -rf scoring/word-sys2")
# subprocess_call("scripts/score.sh lib/kws/word-sys2.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/word-sys2.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/word-sys2.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/word-sys2.xml scoring oov")

# subprocess_call("rm -rf scoring/morph")
# subprocess_call("scripts/score.sh lib/kws/morph.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/morph.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/morph.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map lib/kws/morph.xml scoring oov")

# ################ STO

# normalise_kws_output('lib/kws/word.xml', 'output/word-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/word-gamma1")
# subprocess_call("scripts/score.sh output/word-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/word-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/word-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/word-gamma1.xml scoring oov")

# normalise_kws_output('lib/kws/word-sys2.xml', 'output/word-sys2-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/word-sys2-gamma1")
# subprocess_call("scripts/score.sh output/word-sys2-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/word-sys2-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/word-sys2-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/word-sys2-gamma1.xml scoring oov")

# normalise_kws_output('lib/kws/morph.xml', 'output/morph-gamma1.xml', 1)
# subprocess_call("rm -rf scoring/morph-gamma1")
# subprocess_call("scripts/score.sh output/morph-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/morph-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/morph-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map output/morph-gamma1.xml scoring oov")


##################################################
# Combination
##################################################

# combine_kws('output/decode.xml', 'output/decode-decomposed.xml', 'outputcombined/decode--decode-decomposed.xml')
# subprocess_call("rm -rf scoringcombined/decode--decode-decomposed.xml")
# subprocess_call("scripts/score.sh outputcombined/decode--decode-decomposed.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/decode--decode-decomposed.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/decode--decode-decomposed.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/decode--decode-decomposed.xml scoring oov")


# normalise_kws_output('outputcombined/decode--decode-decomposed.xml', 'outputcombined/decode--decode-decomposed-gamma1.xml', 1)
# subprocess_call("rm -rf scoringcombined/decode--decode-decomposed-gamma1.xml")
# subprocess_call("scripts/score.sh outputcombined/decode--decode-decomposed-gamma1.xml scoring")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/decode--decode-decomposed-gamma1.xml scoring all")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/decode--decode-decomposed-gamma1.xml scoring iv")
# subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/decode--decode-decomposed-gamma1.xml scoring oov")




combine_kws('lib/kws/word.xml', 'lib/kws/word-sys2.xml', 'outputcombined/word--word-sys2.xml')
combine_kws('lib/kws/morph.xml', 'lib/kws/word-sys2.xml', 'outputcombined/morph--word-sys2.xml')
combine_kws('lib/kws/morph.xml', 'lib/kws/word.xml', 'outputcombined/morph--word.xml')
combine_kws('lib/kws/morph--word.xml', 'lib/kws/word-sys2.xml', 'outputcombined/morph--word--word-sys2.xml')
normalise_kws_output('outputcombined/morph--word--word-sys2.xml', 'outputcombined/morph--word--word-sys2-gamma1.xml', 1)
subprocess_call("rm -rf scoringcombined/morph--word--word-sys2.xml")
subprocess_call("scripts/score.sh outputcombined/morph--word--word-sys2.xml scoring")
subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/morph--word--word-sys2.xml scoring all")
subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/morph--word--word-sys2.xml scoring iv")
subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/morph--word--word-sys2.xml scoring oov")



subprocess_call("rm -rf scoringcombined/morph--word--word-sys2-gamma1.xml")
subprocess_call("scripts/score.sh outputcombined/morph--word--word-sys2-gamma1.xml scoring")
subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/morph--word--word-sys2-gamma1.xml scoring all")
subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/morph--word--word-sys2-gamma1.xml scoring iv")
subprocess_call("scripts/termselect.sh lib/terms/ivoov.map outputcombined/morph--word--word-sys2-gamma1.xml scoring oov")









