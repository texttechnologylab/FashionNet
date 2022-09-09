#define class for user Input
#all incoming data from user input sentences will be stored into this class
class userInput:
    def __init__(self,sentences,token, pos_tags, lemmata, stemmer, noun_chunks, entities, general, dependencies, neo_base_data, attributes):
        self.sentences = sentences
        self.token = token
        self.pos_tags = pos_tags
        self.lemmata = lemmata
        self.stemmer = stemmer
        self.noun_chunks = noun_chunks
        self.entities = entities
        self.general = general
        self.dependencies = dependencies
        self.neo_base_data = neo_base_data
        self.attributes = attributes

    #define function to get all data related to one token
    def get_data_single_token(self, token):
        collected_token_data = {}
        collected_token_data["token_id"] = self.token[token]
        collected_token_data["pos_tag"] = self.pos_tags[token]
        collected_token_data["lemmata"] = self.lemmata[token]
        collected_token_data["stemmer"] = self.stemmer[token]
        collected_token_data["dependencies"] = self.dependencies[token]
        collected_token_data["neo_base_data"] = self.neo_base_data[token]
        #its possible that there are no attributes related to a token, therefore "try/except" is used
        try:
            collected_token_data["attributes"] = self.attributes[token]
        except KeyError:
            collected_token_data["attributes"] = None

        return collected_token_data

