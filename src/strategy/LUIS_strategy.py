from dataclasses import replace
from re import I
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

        self.prediction_response = self.client_runtime.prediction.get_slot_prediction(self.config.app_id, "Production", prediction_request, show_all_intents=True, verbose=True)

    
    def recognize_intent(self):
        """function to recognize potential intent

        Returns:
            dict: a dict in the following format
            {
                "top_intent": <name of the intent that has the highest confidence score>,
                "intents": [
                    {
                        "intent": <name of the intent>,
                        "score": <confidence score>
                    },
                    {
                        "intent": <name of the intent>,
                        "score": <confidence score>
                    }
                ]
            }
        """
        

        list_of_intents = []


        for intent in self.prediction_response.prediction.intents:
            list_of_intents.append({"intent": intent, "score": self.prediction_response.prediction.intents.get(intent).score})

        return {"top_intent": self.prediction_response.prediction.top_intent,
                "intents": list_of_intents}
    

    def extract_entity(self):
        """function to extract entity

        Raises:
            KeyError: no such key as "$instance"

        Returns:
            dict: a dict in the following format
            {
                children_level_unprebuilt_entity1:
                {
                    "text": ...
                    "startIndex": ...
                    "endIndex": ...
                },
                children_level_unprebuilt_entity2:
                {
                    "text": ...
                    "startIndex": ...
                    "endIndex": ...
                },
                prebuilt_entity1:
                {
                    ...
                },
                prebuilt_entity2:
                {
                    ...
                },
                ...
            }
        }
        """
        def is_contains_chinese(strs):
            for _char in strs:
                if '\u4e00' <= _char <= '\u9fa5':
                    return True
            return False

        def pop_with_check(key, dict):
            if key in dict:
                dict.pop(key)

        entities = self.prediction_response.prediction.entities


        pop_with_check("$instance", entities)

        ret_dict = {}

        for key in entities:
            if is_contains_chinese(key):
                if isinstance(entities.get(key)[0], dict):
                    current_instance = entities.get(key)[0].get("$instance")
                    if current_instance:
                        for instance_key in current_instance:
                            dict_to_process = current_instance.get(instance_key)[0]
                            dict_to_process["endIndex"] = dict_to_process["startIndex"]+dict_to_process["length"]-1
                            try:
                                pop_with_check("type", dict_to_process)
                                pop_with_check("length", dict_to_process)
                                pop_with_check("score", dict_to_process)
                                pop_with_check("modelTypeId", dict_to_process)
                                pop_with_check("modelType", dict_to_process)
                                pop_with_check("recognitionSources", dict_to_process)
                            except:
                                raise KeyError
                        
                            ret_dict[instance_key] = dict_to_process
            else:
                ret_dict[key] = entities[key]

        return ret_dict
    

    def segment_sentence(self):
        """segment user's input sentence

        Returns:
            dict: a dict of words with their location segmented from user's input in the following format
            {<word>: [<start_location>, <end_location>]}
        """
        pass
        
        

luis = LUIS("打电话")

luis.predict()

print(luis.recognize_intent())
