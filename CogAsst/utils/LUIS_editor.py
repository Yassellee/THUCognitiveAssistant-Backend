from BASE_editor import BASE_editor
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials
import sys, time
sys.path.append("..\..")
from CogAsst.configuration import Config


class LUIS_editor(BASE_editor):
    def __init__(self):
        """a construction function that does nothing but build client
        """
        super().__init__()
        self.config = Config()
        self.client = LUISAuthoringClient(self.config.authoring_endpoint, CognitiveServicesCredentials(self.config.authoring_key))

    
    def add_intent(self, intent_name):
        """add intent to model luis

        Args:
            intent_name (str): name for the intent to be added
        """
        self.client.model.add_intent(self.config.app_id, self.config.version_id, intent_name)

    
    def add_entity(self, entity_name, entity_children=[]):
        """add normal entity to luis model

        Args:
            entity_name (str): top level entity, can be globally duplicated
            entity_children (list, optional): children level entity, cannot be locally duplicated. Defaults to [].
            checkout the example below

        Returns:
            a luis-specified class: needs to be used later if features are needed
        """
        # [ 
        #   {
        #       "name": "Pizza",
        #       "children": [
        #           { "name": "Quantity" },
        #           { "name": "Type" },
        #           { "name": "Size" }
        #        ]
        #   },
        #   {
        #        "name": "Toppings",
        #        "children": [
        #            { "name": "Type" },
        #            { "name": "Quantity" }
        #        ]
        #   }
        # ]
        if entity_children:
            mlEntityDefinition = entity_children
            ret_id = self.client.model.add_entity(self.config.app_id, self.config.version_id, name=entity_name,
                                                  children=mlEntityDefinition)
        else:
            ret_id = self.client.model.add_entity(self.config.app_id, self.config.version_id, name=entity_name)


        ret_object = self.client.model.get_entity(self.config.app_id, self.config.version_id, ret_id)
        return ret_object

    
    def add_prebuilt_entity(self, prebuilt_extractor_name):
        """function to add prebuilt entity to luis model

        Args:
            prebuilt_extractor_name (str): name of the prebuilt entity to be added
        """
        self.client.model.add_prebuilt(self.appId, self.versionId, prebuilt_extractor_names=[prebuilt_extractor_name])


    def add_example_utterance(self, labeled_example_utterance):
        """function to add example utterance to luis model

        Args:
            labeled_example_utterance (dict): checkout the example below
        """
        # labeledExampleUtteranceWithMLEntity = {
        #     "text": "我要申请出校，班级是计03，电话是13433333433，事由类型是出校科研，事由描述是在会议上演讲，往来地点有王府井，日期是二月十四号。",
        #     "intentName": "申请出校",
        #     "entityLabels": [
        #         {
        #             "startCharIndex": 7,
        #             "endCharIndex": 68,
        #             "entityName": "出校",
        #             "children": [
        #                 {
        #                     "startCharIndex": 10,
        #                     "endCharIndex": 12,
        #                     "entityName": "班级",
        #                 },
        #                 {
        #                     "startCharIndex": 34,
        #                     "endCharIndex": 37,
        #                     "entityName": "事由类型",
        #                 },
        #                 {
        #                     "startCharIndex": 44,
        #                     "endCharIndex": 49,
        #                     "entityName": "事由描述",
        #                 },
        #                 {
        #                     "startCharIndex": 56,
        #                     "endCharIndex": 58,
        #                     "entityName": "往来地点",
        #                 },
        #             ]
        #         }
        #     ]
        # }
        self.client.examples.add(self.appId, self.versionId, labeled_example_utterance, {"enableNestedChildren": True})

    
    def add_feature(self, entity_id, phrase_dict, feature_name):
        """add feature for luis model

        Args:
            entity_id (str): id for certain entity
            phrase_dict (dict): content of the feature
            feature_name (str): name of the feature

            checkout the example below for phrase_dict
        """
        # phraseList = {
        #     "enabledForAllModels": False,
        #     "isExchangeable": True,
        #     "name": "QuantityPhraselist",
        #     "phrases": "few,more,extra"
        # }
        self.client.features.add_phrase_list(self.appId, self.versionId, phrase_dict)
        phraseListFeatureDefinition = {"feature_name": feature_name, "model_name": None}
        self.client.features.add_entity_feature(self.appId, self.versionId, entity_id, phraseListFeatureDefinition)


    def train_app(self):
        """ name tells everything
        """

        self.client.train.train_version(self.appId, self.versionId)
        waiting = True
        while waiting:
            info = self.client.train.get_status(self.appId, self.versionId)

            waiting = any(map(lambda x: 'Queued' == x.details.status or 'InProgress' == x.details.status, info))
            if waiting:
                print("Waiting 5 seconds for training to complete...")
                time.sleep(5)
            else:
                print("trained")
                waiting = False


    def publish_app(self):
        """name tells everything
        """
        self.client.apps.update_settings(self.appId, is_public=True)

        self.client.apps.publish(self.appId, self.versionId, is_staging=False)