import metapy

parser = metapy.parser.Parser("parser/")

doc = metapy.index.Document()
doc.content("I said that I can't believe that it only costs $19.95! I could only find it for more than $30 before.")

tagger = metapy.sequence.PerceptronTagger("perceptron-tagger/")

tok = metapy.analyzers.ICUTokenizer() # keep sentence boundaries!
tok = metapy.analyzers.PennTreebankNormalizer(tok)
tok.set_content(doc.content())
[token for token in tok]

def extract_sequences(tok):
    sequences = []
    for token in tok:
        if token == '<s>':
            sequences.append(metapy.sequence.Sequence())
        elif token != '</s>':
            sequences[-1].add_symbol(token)            
    return sequences

tok.set_content(doc.content())
for seq in extract_sequences(tok):
    tagger.tag(seq)
    print(seq)

print(' '.join([obs.symbol for obs in seq]))
print(seq)
tree = parser.parse(seq)
print(tree.pretty_str())