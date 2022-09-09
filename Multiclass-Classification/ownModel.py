import os
#dont show warnings and info from tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from transformers import BertTokenizer
import numpy as np
import csv
import random





#dictionary to get text from id
articleDict = {}

#input article mapping to dissolve ids to article type name
with (open("./Text-Vorverarbeitung BERT-Modell/bertData_categoryMapping.csv","r", encoding="utf8", newline="")) as csvFile:
    csvreader = csv.reader(csvFile,delimiter=",")
    for row in csvreader:
        articleDict[row[1]] = row[0]

inputSentence = ""
valid = False
initQ = False
initClass = None

# use user input or test-data
while valid == False:
    initialQuest = input(
        "Do you want to input your own text or use a sample text?\n Type 'user' for your own input or 'sample' for sample-text.\n")
    if initialQuest == "user":
        inputSentence = input("Please input your own text:\n")
        valid = True
    elif initialQuest =="sample":
        pick = random.randint(0,44469)
        # input article mapping to dissolve ids to article type name
        with (open("bertData.csv", "r", encoding="utf8", newline="")) as csvFile:
            csvreader = csv.reader(csvFile, delimiter=",")
            for ind,row in enumerate(csvreader):
                if ind == pick:
                    if len(row) == 3:
                        inputSentence = row[2]
                        initClass = row[1]
                        initQ = True
                        break
                    else:
                        pick += 1
                        continue
                else:
                    continue
        print("Calculation begins. Picked one random description from dataset.\n")
        print("The text is:\n")
        print(inputSentence)
        valid = True
    else:
        continue

#load fine-tuned model
model = tf.keras.models.load_model("category_model")
#print(model.summary())

#use bert-tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

#preprocess data to use on own model
def prep_data(text):
    tokens = tokenizer.encode_plus(text, max_length=512,
                                   truncation=True,
                                   padding="max_length",
                                   add_special_tokens=True,
                                   return_token_type_ids=False,
                                   return_tensors="tf")
    return {
        "input_ids": tf.cast(tokens["input_ids"], tf.float64),
        "attention_mask": tf.cast(tokens["attention_mask"], tf.float64)
    }



data = prep_data(inputSentence)
probs = model.predict(data)
probsID = np.argmax(probs[0])
print("The model predict the article-type: " + articleDict[str(probsID)])
if initQ == True:
    print("The labeled class of this sample text is: " + articleDict[initClass])
    if str(probsID) == initClass:
        print("The model predicted the class right.")
    else:
        print("The model predicted the class wrong.")


