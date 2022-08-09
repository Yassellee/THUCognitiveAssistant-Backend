class BASE_editor:
    def __init__(self):
        pass


    def add_intent(self, intent_name):
        raise NotImplementedError


    def add_entity(self, entity_name, entity_children=[]):
        raise NotImplementedError
        

    def add_prebuilt_entity(self, prebuilt_extractor_name):
        raise NotImplementedError
        

    def add_example_utterance(self, labeled_example_utterance):
        raise NotImplementedError


    def train_app(self):
        raise NotImplementedError


    def publish_app(self):
        raise NotImplementedError

