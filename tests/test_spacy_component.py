from fastcoref import spacy_component
import spacy


texts = ['We are so happy to see you using our coref package. This package is very fast!',
         'Glad to see you are using the spacy component as well. As it is a new feature!',
         'The man tried to put the boot on his foot but it was too small.',
         'Alice goes down the rabbit hole. Where she would discover a new reality beyond her expectations.'
        ]

# FCoref

# Test default values
nlp_fcoref = spacy.load("en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"])   # Resolving text requires pos tagging
nlp_fcoref.add_pipe("fastcoref")
doc = nlp_fcoref(texts[0])
print(doc._.coref_clusters)

# Test not default values
nlp_fcoref = spacy.load("en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"])
nlp_fcoref.add_pipe(
    "fastcoref",
    config={'model_architecture': 'FCoref', 'model_path': 'biu-nlp/f-coref', 'device': 'cpu'}
)
doc = nlp_fcoref(texts[0])
assert doc._.resolved_text == ''
print(doc._.coref_clusters)

# Test pipe while not returning resolved text
doc_list = nlp_fcoref.pipe(texts)
for doc in doc_list:
    assert doc._.resolved_text == ''
    print(doc._.coref_clusters)

# Test pipe while returning resolved text
doc_list = nlp_fcoref.pipe(texts, component_cfg={"fastcoref": {'resolve_text': True}})
for doc in doc_list:
    print(doc._.resolved_text)
    print(doc._.coref_clusters)

input_text = "The social media company BlueBird Inc. just acquired an AI company called DataMind Solutions for $4.7 billion. BlueBird wants to use DataMind's innovative technology to make their social media sites even better and more personalized for users. This deal is making waves in the tech world and could change the way we use social media in the future."
expected_output = "The social media company BlueBird Inc. just acquired an AI company called DataMind Solutions for $4.7 billion. BlueBird wants to use DataMind's innovative technology to make The social media company BlueBird Inc.'s social media sites even better and more personalized for users. This deal is making waves in the tech world and could change the way we use social media in the future."
doc = nlp_fcoref(input_text, component_cfg={"fastcoref": {"resolve_text": True}})
print(f"{doc._.resolved_text=}")
print(f"{expected_output=}")
assert doc._.resolved_text == expected_output

# LingMess

# Test not default values
nlp_fcoref = spacy.load("en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"])
nlp_fcoref.add_pipe(
    "fastcoref",
    config={'model_architecture': 'LingMessCoref', 'model_path': 'biu-nlp/lingmess-coref', 'device': 'cpu'}
)
doc = nlp_fcoref(texts[0])
assert doc._.resolved_text == ''
print(doc._.coref_clusters)

# Test pipe while not returning resolved text
doc_list = nlp_fcoref.pipe(texts)
for doc in doc_list:
    assert doc._.resolved_text == ''
    print(doc._.coref_clusters)

# Test pipe while returning resolved text
doc_list = nlp_fcoref.pipe(texts, component_cfg={"fastcoref": {'resolve_text': True}})
for doc in doc_list:
    print(doc._.resolved_text)
    print(doc._.coref_clusters)
