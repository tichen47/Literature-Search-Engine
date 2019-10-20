import metapy
 
metapy.log_to_stderr()

doc = metapy.index.Document()
doc.content("I said that I can't believe that it only costs $19.95!")

# TODO: Configuration for analyzers

# 1. remove XML tag
tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
# 2. setup token length
tok = metapy.analyzers.LengthFilter(tok, min=2, max=30)
# 3. remove stop words, TODO: Download the file, put it on server
# tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)


tok.set_content(doc.content()) # this could be any string
print([token for token in tok])


# getNext()