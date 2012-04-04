corpus = korpusnamn
original_dir = original
files := $(basename $(notdir $(wildcard $(original_dir)/*.xml)))

vrt_annotations = word sentence.n paragraph.n sentence.id  text.title n
vrt_columns     = word -          -           -            -          -
vrt_structs     = -    sentence:n paragraph:n sentence:id  text:title -

xml_elements    = para
xml_annotations = paragraph
xml_skip = preamble doc rtf-definition font-table font-in-table color-table color-in-table style-table paragraph-style

include /export/res/lb/korpus/material/Makefile.common

token_chunk = sentence
token_segmenter = punkt_word

sentence_chunk = paragraph
sentence_segmenter = punkt_sentence
sentence_model = $(punkt_model)

sentence_order = position

paragraph_chunk = text
paragraph_segmenter = blanklines


xml_headers            = doc.preamble.doc-information.title:TEXT
xml_header_annotations = token.text.title

#                                  RULES                                       #
################################################################################

include /export/res/lb/korpus/material/Makefile.rules
