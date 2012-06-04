from lxml import etree


dtd = etree.DTD("lexiconinfo/DTD_LMF_REV_16.dtd")
#lexicon = open('../../Lexicon/schlyter.xml','r').read()
#lexicon = open('../../Lexicon/soederwall_ny/soederwall_main_NYAST.xml','r').read()
#lexicon = open('../../Lexicon/soederwall_ny/soederwall_supp_NYAST.xml','r').read()
#lexicon = open('../../Lexicon/good/lmf/soederwall_supp/soederwall_supp.xml','r').read()
#lexicon = open('testit2.xml','r').read()
#lexicon = open('kast.xml','r').read()
#lexicon = open('lexiconinfo/newer/soederwall_main.xml','r').read()
#lexicon = open('lexiconinfo/newer/soederwall_supp.xml','r').read()
lexicon = open('lexiconinfo/newer/schlyter.xml','r').read()
root = etree.XML(lexicon)
print(dtd.validate(root))
def why(n=100):
 print(dtd.error_log.filter_from_errors()[:n])
# True

