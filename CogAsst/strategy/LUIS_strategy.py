import os, sys
basedir = os.path.abspath(os.path.dirname(__file__))
os.chdir(basedir)
sys.path.append(basedir)
from BASE_strategy import BASE
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

        self.prediction_response = self.client_runtime.prediction.get_slot_prediction(self.config.app_id, "Production", prediction_request)

    
    def recognize_intent(self):
        """function to recognize potential intent

        Returns:
            dict: a dict in the following format
            {
            "top_intent": <name of the intent that has the highest confidence score>,
            "intents": {
                <Intent1>: {
                    "score": <score of intent1>
                },
                <Intent2>: {
                    "score": <score of intent2>
                },
                ......(intents are ranked by their scores, from high to low)
            }
        """

        return {"top_intent": self.prediction_response.prediction.top_intent,
                "intents": self.prediction_response.prediction.intents}
    

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
            list: a list of all possible word segmented from user's input
        """
        seg_list = jieba.cut(self.input_sentence, cut_all=True)
        return list(seg_list)


# test = LUIS("我要预定八月一日综体的羽毛球馆")
# test.predict()
# print(test.recognize_intent())
# print(test.extract_entity())
# print(test.segment_sentence())
