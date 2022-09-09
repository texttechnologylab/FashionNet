[![version](https://img.shields.io/github/license/texttechnologylab/FashionNet)]()


# FashionNet
FashionNet extracts clothing items occurring in a text based on a Neo4J knowledge base that has also been made available. 
The knowledge base was developed based on a specially trained BERT model and also feeds from other resources such as wikidata, wordnet, and similarity relations between items via static word models ([Word2Vec](https://github.com/tensorflow/docs/blob/master/site/en/tutorials/text/word2vec.ipynb), [GLove](https://nlp.stanford.edu/projects/glove/), and [fastText](https://fasttext.cc/)) and the bidirectional [BERT model](https://github.com/google-research/bert).

This program was developed as part of the master's thesis "Situationsabhängige Bekleidungsmodellierung mit Hilfe von Machine Learning für die Erstellung von Avataren (german)".

## General Information

Necessary programs:
- [Python 3](https://www.python.org/downloads/)
- [Neo4J](https://neo4j.com/)
- 

## Usage - Multiclass-Classification


## Usage - Clothingitems-Prediction
To run the prediction model, it is necessary to include the knowledge base in Neo4J and start the database. Then the Python program main.py can be started and any text can be entered. The results are then output in the console.

