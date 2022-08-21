class Config:
    def __init__(self):

        """
        cognitive strategy chosen,
        currently only LUIS is supported
        """
        self.cognitive_strategy = "LUIS"

        """
        LUIS related configuration attributes
        """
        self.authoring_key = 'd96fedab58f04889805b7a92be2068fa'
        self.authoring_endpoint = 'https://patpat-authoring.cognitiveservices.azure.com/'
        self.prediction_key = '15127511d79c4d0289cfb87d48ee40c7'
        self.prediction_endpoint = 'https://australiaeast.api.cognitive.microsoft.com/'
        self.app_name = "AutoPat"
        self.version_id = "0.1"
        self.app_id = "bf2c83c3-61b9-48af-8977-bb7a51b0d002"

