import metapy

metapy.log_to_stderr()

doc = metapy.index.Document()
doc.content("I said that I can't believe that it only costs $19.95!")

tok = metapy.analyzers.ICUTokenizer()
tok.set_content(doc.content()) # this could be any string
print([token for token in tok])


# getNext()