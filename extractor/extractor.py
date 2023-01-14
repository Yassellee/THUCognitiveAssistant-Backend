from pprint import pprint
from paddlenlp import Taskflow
import time


class extractor:
    def __init__(self, finetuned_model_path = None, pretrained_mode_name = "uie-base", schema = None):
        self.finetuned_model_path = finetuned_model_path
        self.pretrained_mode_name = pretrained_mode_name
        if schema is None:
            raise Exception("schema is None")
        self.schema = schema
        if finetuned_model_path is None:
            self.model = Taskflow("information_extraction", model=self.pretrained_mode_name, schema=self.schema)
        else:
            self.model = Taskflow("information_extraction", task_path=finetuned_model_path, schema=self.schema)
   
    def extract_single(self, text):
        return self.model(text)

    def extract_batch(self, texts):
        return self.model(texts)


class summarizer:
    def __init__(self, finetuned_model_path = None, pretrained_mode_name = "uie-base", schema = None):
        self.finetuned_model_path = finetuned_model_path
        self.pretrained_mode_name = pretrained_mode_name
        if schema is None:
            raise Exception("schema is None")
        self.schema = schema
        if finetuned_model_path is None:
            self.model = Taskflow("information_extraction", model=self.pretrained_mode_name, schema=self.schema)
        else:
            self.model = Taskflow("information_extraction", task_path=finetuned_model_path, schema=self.schema)
   
    def extract_single(self, text):
        return self.model(text)

    def extract_batch(self, texts):
        return self.model(texts)


def demo():
    schema = ["人名", "食堂名称", "起始站", "终点站", "商品类别"]
    local_extractor = extractor(schema=schema, finetuned_model_path="checkpoint/model_best")
    texts = ["与张三去紫荆吃饭", 
    "我要买一张从北京到上海的高铁票",
    "我要买一件长款大衣"]
    start = time.time()
    local_extractor.model.set_schema(schema)
    result = local_extractor.extract_batch(texts)
    end = time.time()
    print("time cost: ", end - start)
    pprint(result)


if __name__ == "__main__":
    demo()
        