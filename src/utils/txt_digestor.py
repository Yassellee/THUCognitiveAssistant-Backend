import codecs, re, json


input_file_path = "..\\..\\data\\local_luis.txt"


def digest_file(file_path):
    """function to digest a txt file

    Args:
        file_path (str): path to the txt file

    Returns:
        list: a list of strings
    """
    with codecs.open(file_path, 'r', 'utf-8') as f:
        lines = f.readlines()
        return lines


def digest_intent(lines):
    """function to digest intent

    Args:
        lines (list): a list of strings

    Returns:
        dict: a dict in the following format
        {
            "intent1": ["sentence1", "sentence2"],
            "intent2": ["sentence1", "sentence2"]
        }
    """
    intent_dict = {}
    for line in lines:
        line = line.strip("\n").strip("\r")
        line = line.split(':')
        if intent_dict.get(line[0]) is None:
            intent_dict[line[0]] = []
        intent_dict[line[0]].append(line[1])
    return intent_dict

def digest_intent_dict(intent_dict):
    """function to digest intent_dict

    Args:
        intent_dict (dict): a dict in the following format
        {
            "intent1": ["sentence1", "sentence2"],
            "intent2": ["sentence1", "sentence2"]
        }

    Returns:
        intent2entity, a dict in the following format
        {
            "intent1": ["entity1", "entity2"],
            "intent2": ["entity3", "entity4"]
        },
        labeled_utterances, a list in the following format
        [
            {
                "text": "sentence1",
                "intentName": "intent1",
                "entityLabels": 
                [
                    {
                        "startCharIndex": start_index,
                        "endCharIndex": end_index,
                        "entityName": "entity1"
                    },
                    {
                        "startCharIndex": start_index,
                        "endCharIndex": end_index,
                        "entityName": "entity2"
                    }
                ]
            },
            {
                "text": "sentence2",
                "intentName": "intent1",
                "entityLabels":
                [
                    {
                        "startCharIndex": start_index,
                        "endCharIndex": end_index,
                        "entityName": "entity1"
                    },
                    {
                        "startCharIndex": start_index,
                        "endCharIndex": end_index,
                        "entityName": "entity2"
                    }
                ]
            }
        ],
        entity2feature, a dict in the following format
        {
            "entity1": ["feature1", "feature2"],
            "entity2": ["feature3", "feature4"]
        },
        entity_list, a list of entities
    """
    intent2entity = {}
    labeled_utterances = []
    luis_labeled_utterances = []
    entity2feature = {}
    entity_list = []
    entity_to_id = {}
    classifier_data = []

    cnt = 0

    for intent in intent_dict:
        first_sentence = intent_dict[intent][0]
        entity_with_content = re.compile(r"<.*?>").findall(first_sentence)
        for i in range(len(entity_with_content)):
            entity_with_content[i] = entity_with_content[i].strip("<").strip(">")
        for entity in entity_with_content:
            current_entity = entity.split('=')[0]
            entity_list.append(current_entity)
            if intent2entity.get(intent) is None:
                intent2entity[intent] = []
            intent2entity[intent].append(current_entity)
            if '/' in entity:
                current_feature = entity.split('=')[1].split('|')[1].split('/')
                entity2feature[current_entity] = current_feature

        for sentence in intent_dict[intent]:
            local_entity_with_content = re.compile(r"<.*?>").findall(sentence)
            for i in range(len(local_entity_with_content)):
                local_entity_with_content[i] = local_entity_with_content[i].strip("<").strip(">")
            for entity in local_entity_with_content:
                current_content = re.split(r"[=, |]", entity)[1]
                sentence = sentence.replace("<"+entity+">", current_content)
                if entity_to_id.get(current_content) is None:
                    entity_to_id[current_content] = len(entity_to_id)
            current_labeled_utterance = {
                "id" : cnt,
                "text": sentence,
                "relations": [],
                "entities": []
            }
            current_classifier_data = {
                "text": sentence,
                "label": intent
            }
            cnt += 1
            for entity in local_entity_with_content:
                current_entity = entity.split('=')[0]
                current_content = re.split(r"[=, |]", entity)[1]
                current_start_index = sentence.index(current_content)
                current_end_index = current_start_index + len(current_content)
                current_labeled_utterance["entities"].append(
                    {
                        "id": entity_to_id[current_content],
                        "start_offset": current_start_index,
                        "end_offset": current_end_index,
                        "label": current_entity
                    }
                )
            labeled_utterances.append(current_labeled_utterance)
            classifier_data.append(current_classifier_data)

        for sentence in intent_dict[intent]:
            local_entity_with_content = re.compile(r"<.*?>").findall(sentence)
            for i in range(len(local_entity_with_content)):
                local_entity_with_content[i] = local_entity_with_content[i].strip("<").strip(">")
            for entity in local_entity_with_content:
                current_content = re.split(r"[=, |]", entity)[1]
                sentence = sentence.replace("<"+entity+">", current_content)
            current_labeled_utterance = {
                "text": sentence,
                "intentName": intent,
                "entityLabels": []
            }
            for entity in local_entity_with_content:
                current_entity = entity.split('=')[0]
                current_content = re.split(r"[=, |]", entity)[1]
                current_start_index = sentence.index(current_content)
                current_end_index = current_start_index + len(current_content)
                current_labeled_utterance["entityLabels"].append(
                    {
                        "startCharIndex": current_start_index,
                        "endCharIndex": current_end_index-1,
                        "entityName": current_entity
                    }
                )
            luis_labeled_utterances.append(current_labeled_utterance)

    entity_list = list(set(entity_list))

    return intent2entity, labeled_utterances, entity2feature, entity_list, classifier_data, luis_labeled_utterances


def main():
    lines = digest_file(input_file_path)
    intent_dict = digest_intent(lines)
    intent2entity, labeled_utterances, entity2feature, entity_list, classifier_data, luis_labeled_utterances = digest_intent_dict(intent_dict)

    with codecs.open("..\\..\\data\\intent2entity.json", 'w', 'utf-8') as f:
        json.dump(intent2entity, f, ensure_ascii=False, indent=4)
    with codecs.open("..\\..\\data\\labeled_utterances.json", 'w', 'utf-8') as f:
        json.dump(labeled_utterances, f, ensure_ascii=False, indent=4)
    with codecs.open("..\\..\\data\\entity2feature.json", 'w', 'utf-8') as f:
        json.dump(entity2feature, f, ensure_ascii=False, indent=4)
    with codecs.open("..\\..\\data\\entity_list.json", 'w', 'utf-8') as f: 
        json.dump(entity_list, f, ensure_ascii=False, indent=4)
    with codecs.open("..\\..\\data\\train.txt", 'w', 'utf-8') as f:
        for line in classifier_data:
            f.write(line["text"]+"\t"+line["label"]+"\n")
    with codecs.open("..\\..\\data\\dev.txt", 'w', 'utf-8') as f:
        for line in classifier_data:
            f.write(line["text"]+"\t"+line["label"]+"\n")
    with codecs.open("..\\..\\data\\label.txt", 'w', 'utf-8') as f:
        for intent in intent2entity:
            f.write(intent+"\n")
    with codecs.open("..\\..\\data\\luis_labeled_utterances.json", 'w', 'utf-8') as f:
        json.dump(luis_labeled_utterances, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()