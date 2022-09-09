import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#import self-written module to access different neo4j-queries (self-made)
import query_neo4j
#import self-written classes (self-made)
import fashionnet_classes
#import spaCy for tokenization & POS-tagging
import spacy
#import re to remove punctuation in input sentence
import re
#import stemmer module to get stemmer of each word in input sentence
from nltk.stem.snowball import SnowballStemmer
#sentence tokenizer
from nltk import tokenize

#load english tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

#load english stemmer
stemmer = SnowballStemmer(language="english")

#s = "The girl on the bench wears fancy red shoe, blue jean and a nice shirt."


def countList(lst1, lst2):
    return [sub[item] for item in range(len(lst2))
                      for sub in [lst1, lst2]]

#function to preprocess input data from user and create instance of userInput (fashionnet_classes.py)
def preprocessing_input(sentence):

    #delete all punctuation in sentence
    no_punc = re.sub(r'[^\w\s]','',sentence)

    #get spaCy object for sentence
    input_sentence = nlp(no_punc)

    #dictionary that provides all calculated information about the input sentence
    information = {}

    #calculate pos-tags for every given word in input sentence
    information["token_id"] = {}
    information["pos_tags"] = {}
    information["lemmata"] = {}
    information["stemmer"] = {}
    information["attributes"] = {}
    for ind,word in enumerate(input_sentence):
        information["token_id"][word.text] = ind
        information["pos_tags"][word.text] = word.pos_
        #print(word.text, word.pos_)
        information["lemmata"][word.text] = word.lemma_
        information["stemmer"][word.text] = stemmer.stem(word.text)
    #calculate noun-chunks given in input sentence
    information["noun_chunks"] = {}
    for ind, noun in enumerate(input_sentence.noun_chunks):
        information["noun_chunks"][ind] = noun.text
        #print(noun.text)

    #list all entities identified in input sentence
    information["entities"] = {}
    for entity in input_sentence.ents:
        information["entities"][entity.text] = entity.label_

    #get dependency values for each token in input sentence
    information["dependencies"] = {}
    dep_tag = [[token.dep_,token.text] for token in input_sentence]
    for d in dep_tag:
        information["dependencies"][d[1]] = d[0]

    #providing some general information about input sentence
    information["general"] = {}
    information["general"]["amount_of_words"] = len(input_sentence)

    #get base data for each token from neo4j-database if available
    information["neo_base_data"] = {}
    for word in input_sentence:
        word_neo_data = query_neo4j.get_nodeData(word.text)
        #check if result from query is empty or not
        if not word_neo_data:
            stemmer_neo_data = query_neo4j.get_nodeData(stemmer.stem(word.text))
            if not stemmer_neo_data:
                #if result is empty assign to None
                information["neo_base_data"][word.text] = None
            else:
                # otherwise assign word.text to responded result
                information["neo_base_data"][word.text] = stemmer_neo_data
        else:
            #otherwise assign word.text to responded result
            information["neo_base_data"][word.text] = word_neo_data

    #get 2-word dependencies (attributes) for each token
    tok_l = input_sentence.to_json()["tokens"]
    for word in tok_l:
        head = tok_l[word["head"]]
        #print(word["dep"])
        if word["dep"] == 'amod':
            information["attributes"][no_punc[word["start"]:word["end"]]] = no_punc[head["start"]:head["end"]]
        else:
            information["attributes"][no_punc[word["start"]:word["end"]]] = None
    old_attr = information["attributes"]
    new_attr = {}
    for key, value in old_attr.items():
        if value in new_attr:
            new_attr[value].append(key)
        else:
            new_attr[value] = [key]
    information["attributes"] = new_attr
    sentence_info = fashionnet_classes.userInput(1,
                                                 information["token_id"],
                                                 information["pos_tags"],
                                                 information["lemmata"],
                                                 information["stemmer"],
                                                 information["noun_chunks"],
                                                 information["entities"],
                                                 information["general"],
                                                 information["dependencies"],
                                                 information["neo_base_data"],
                                                 information["attributes"])

    return information, sentence_info


###################### for final UserInput ######################

active = True

#get input from user
while(active):
    user_input = input("Please input a description text of clothing. \nThe programm will calculate what clothing articles are described.\nInput 'exit' to close the programm.\n\n")
    if user_input == "exit":
        active = False
        break
    else:
        res = preprocessing_input(user_input)

        #get class properties for input sentence
        #res = preprocessing_input(s)
        dict_view = res[0]
        class_view =res[1]
        #print(dict_view)


        # delete all punctuation in sentence
        no_punc = re.sub(r'[^\w\s]', '', user_input)
        # get spaCy object for sentence
        input_sentence = nlp(no_punc)

        #indicates if items where found or not
        hit = False

        #indirect Hits
        potential_nodes = []
        #direct hits
        clothing_nodes = []
        for word in input_sentence:
            wordData = class_view.get_data_single_token(word.text)
            if wordData["neo_base_data"] != None:
                hit = True
                node = wordData["neo_base_data"][0]["n"]["name"]
                node_label = query_neo4j.get_nodeLabel(node)
                #print(node_label)
                #potentialClothes = []
                if node_label != "CLOTHING" and node_label != "COLOR":
                    clothing_path = query_neo4j.get_shortestPathToClothesWithoutBERT(node)
                    potential_nodes.append(clothing_path)
                if node_label == "CLOTHING":
                    clothing_details = query_neo4j.get_clothingDetails(node)
                    tokenData = class_view.get_data_single_token(word.text)
                    clothing_nodes.append([clothing_details,tokenData["attributes"],word.text])
        #print(clothing_nodes)
        if hit == True:
            print("_______________")
            print("Detected Items: " + str(len(clothing_nodes)) + "\n")
            for ind,i in enumerate(clothing_nodes):
                print(str(ind+1))
                print("Name: " + i[2])
                try:
                    print("Associated Attributes: " + i[1][0] + "\n")
                except TypeError:
                    print("Attributes: No data found.")
                print("\nItem-Properties: ")
                try:
                    print("AgeGroup: " + i[0][0]["AgeGroup"])
                except TypeError:
                    print("AgeGroup: No data available")
                try:
                    print("Gender: " + i[0][0]["Gender"])
                except TypeError:
                    print("Gender: No data available")
                try:
                    print("Category: " + i[0][0]["Category"])
                except TypeError:
                    print("Category: No data available")
                try:
                    print("Sub-Category: " + i[0][0]["SubCategory"])
                except:
                    print("Sub-Category: No data available")

                print("\n")
            print("_______________")
            print("Potential Items: " + str(len(potential_nodes)) + "\n")
            for ind,j in enumerate(potential_nodes):
                print(str(ind+1))
                print("Target-Name: " + j[0]["targets"][0])
                print("Source-Name: " + str(j[0]["NodePath"][0]))
                print("Path-length: " + str(j[0]["l"]))
                print("Node-Path: " + str(j[0]["NodePath"]))
                print("Relationship-Path: " + str(j[0]["RelationshipPath"]))
                print("\n_______________________________________________________")
        else:
            print("Nothing found in this sentence.\n_______________________________________________________")








