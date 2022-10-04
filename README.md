[![version](https://img.shields.io/github/license/texttechnologylab/FashionNet)]()


# FashionNet
FashionNet extracts clothing items occurring in a text based on a Neo4J knowledge base that has also been made available. 
The knowledge base was developed based on a specially trained BERT model and also feeds from other resources such as wikidata, wordnet, and similarity relations between items via static word models ([Word2Vec](https://github.com/tensorflow/docs/blob/master/site/en/tutorials/text/word2vec.ipynb), [GLove](https://nlp.stanford.edu/projects/glove/), and [fastText](https://fasttext.cc/)) and the bidirectional [BERT model](https://github.com/google-research/bert).

This program was developed as part of the master's thesis "Situationsabhängige Bekleidungsmodellierung mit Hilfe von Machine Learning für die Erstellung von Avataren (german)".

## General Information - Clothing-Prediction
Install:
- [Python 3](https://www.python.org/downloads/)
- [Neo4J](https://neo4j.com/)

python-pockages:
- os
- spacy
- re
- from nltk.stem.snowball import SnowballStemmer
- from neo4j import GraphDatabase

### Run - Clothing-Prediction
- make sure to run Neo4J-database, otherwise the program has no access to the data.
- run main.py from development environment (i.e. PyCharm) or console via command python main.py)

### Usage - Clothing-Prediction
Any text can be entered. The results are then displayed in console.

### Sample output

input-sentence: "The girl on the bench wears fancy red high heels and a blue jeans."

Detected Items: 1
name: jeans
Associated Attributes: blue
--> Item-Properties (jeans):
AgeGroup: [['adults-men','86.57%'],['adults-women',9.14%'],...]
Gender: [['Men','88.41%'],['Women','9,14%'],...]
Category: Apparel
Sub-Category: Topwear

Potenital Items: 1
Target-Name: shoes
Source-name: high-heels
path-length: 2
node-path: ['high heels', 'heels','shoes']
relationship-path: ['BMF_IDF','BMF_IDF']


## General Information - Multiclass-Classification
- https://docs.conda.io/en/latest/miniconda.html (install and run conda-prompt)
- conda create -n 'bertModel' python=3.8
- conda activate bertModel
- pip install tensorflow
- pip install transfomers
- pip install numpy

### Run - Multiclass-Classification
- navigate to bertModel.py file direction
- python ownModel.py

### Usage - Multiclass-Classification
- follow instructions on command line
- there are two possible usages. It's possible to use a random sample text from (Fashion Product Image Dataset, Kaggle) or input sentences by yourself

# Cite
Meyer, D.,(2022,September). Situationsabhängige Bekleidungsmodellierung mit Hilfe von Machine Learning für die Erstellung von Avataren. 

# BibTex
