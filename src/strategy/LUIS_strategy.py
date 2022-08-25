from BASE_strategy import BASE
import sys, json
sys.path.append("..\..")
from configuration import Config
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
import jieba


class LUIS(BASE):
    def __init__(self, input_sentence):
        """construction funciton for LUIS
        using BASE construction function

        Args:
            input_sentence (str): user's input sentence
        """
        super().__init__(input_sentence=input_sentence)
        self.config = Config()
        runtime_credentials = CognitiveServicesCredentials(self.config.prediction_key)
        self.client_runtime = LUISRuntimeClient(endpoint=self.config.prediction_endpoint, credentials=runtime_credentials)

    
    def predict(self):
        """use LUIS to digest user's input sentence
        """
        prediction_request = {"query": self.input_sentence}

        self.prediction_response = self.client_runtime.prediction.get_slot_prediction(self.config.app_id, "Production", prediction_request, show_all_intents=True)

    
    def recognize_intent(self):
        """function to recognize potential intent

        Returns:
            dict: a dict in the following format
            {
            "top_intent": <name of the intent that has the highest confidence score>,
            "intents": [<Intent1>, <Intent2>], alist of intents ranked by their confidence scores
        """
        

        list_of_intents = []

        for intent in self.prediction_response.prediction.intents:
            list_of_intents.append(intent)

        return {"top_intent": self.prediction_response.prediction.top_intent,
                "intents": list_of_intents}
    

    def extract_entity(self):
        """function to extract entity

        Raises:
            KeyError: no such key as "$instance"

        Returns:
            dict: a dict in the following format
            {
                "<top level entity>": [
                    {
                        "<second level entity 1>": [
                            <data of the second level entity 1>
                        ],
                        "<second level entity 2>": [
                            <data of the second level entity 2>
                        ],
                        ......
                    }
                ]
            }
        }
        """
        entities = self.prediction_response.prediction.entities

        for key in entities:
            if "$instance" in entities[key]:
                try:
                    entities[key].pop("$instance")
                except:
                    raise KeyError
        
        return entities
    

    def segment_sentence(self):
        """segment user's input sentence

        Returns:
            dict: a dict of words with their location segmented from user's input in the following format
            {<word>: [<start_location>, <end_location>]}
        """
        word_location = {}
        result = jieba.tokenize(self.input_sentence)
        for token in result:
            word_location[token[0]] = [token[1], token[2]]
        
        return word_location
        

luis = LUIS("我要预约八月十号的综体羽毛球馆。")

luis.predict()

print(luis.segment_sentence())
