class BASE:
    def __init__(self, input_sentence):
        """initialize BASE as base class for strategies

        Args:
            input_sentence (str): user's input sentence
        """
        self.input_sentence = input_sentence

    
    def predict(self):
        raise NotImplementedError


    def recognize_intent(self):
        raise NotImplementedError
    

    def extract_entity(self):
        raise NotImplementedError

    
    def segment_sentence(self):
        raise NotImplementedError

