[![version](https://img.shields.io/github/license/texttechnologylab/FashionNet)]()


# FashionNet
FashionNet extracts clothing items occurring in a text based on a Neo4J knowledge base that has also been made available. 
The knowledge base was developed based on a specially trained BERT model and also feeds from other resources such as wikidata, wordnet, and similarity relations between items via static word models ([Word2Vec](https://github.com/tensorflow/docs/blob/master/site/en/tutorials/text/word2vec.ipynb), [GLove](https://nlp.stanford.edu/projects/glove/), and [fastText](https://fasttext.cc/)) and the bidirectional [BERT model](https://github.com/google-research/bert).

This program was developed as part of the master's thesis "Situationsabhängige Bekleidungsmodellierung mit Hilfe von Machine Learning für die Erstellung von Avataren (german)".


## General Information - Clothing-item-prediction
Install:
- [Python 3](https://www.python.org/downloads/)
- [Neo4J](https://neo4j.com/)

### Run - Clothing-item-prediction
- make sure to run Neo4J-database, otherwise the program has no access to the data.
- run main.py from development environment (i.e. PyCharm) or console via command python main.py)

### Usage - Clothing-items-Prediction
Any text can be entered. The results are then displayed in console.



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


