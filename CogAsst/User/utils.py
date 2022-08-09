from User.models import *
from Intent.models import *
import json
import ast

def update_state(id, state):
    tmp_user = User.objects.get(username = id)
    tmp_user.state = state
    tmp_user.save()

def getParamToAsked(entity_, matchedEntity, tgt_user):
    print(entity_)
    print(matchedEntity)
    entity = ast.literal_eval(entity_)
    keys = list(entity.keys())
    paramToAsk = []
    for key in keys:
        if key in matchedEntity:
            if entity[key] != 0:
                paramToAsk += [item for item in entity[key] if (item not in matchedEntity[key][0])]  
        else:
            if entity[key] != 0:
                paramToAsk.append(item for item in entity[key])
            else:
                paramToAsk.append(key)
    print(paramToAsk)
    tgt_user.paramToAsk = paramToAsk
    tgt_user.save()
    return paramToAsk


# update paramToAsk list and matchedEntity, return the new paramToAsk list
def get_paramToAsk(tgt_user, message):
    entity_ = Intent.objects.filter(name = tgt_user.intent).first().entity
    matchedEntity = ast.literal_eval(tgt_user.matchedEntity)
    entity = ast.literal_eval(entity_)
    keys = list(entity.keys())
    pre_param = ast.literal_eval(tgt_user.paramToAsk)[0]
    print(pre_param)
    for key in keys:
        if key in matchedEntity:
            if pre_param in entity[key] :
                print(matchedEntity[key])
                matchedEntity[key][0][pre_param] = [message] 
        else:
            if entity[key] != 0:
                if pre_param in entity[key] :
                    matchedEntity[key] = [{}]
                    matchedEntity[key][0][pre_param] = [message] 
            else:
                if pre_param == key:
                    matchedEntity[key] = message
    tgt_user.paramToAsk = str(ast.literal_eval(tgt_user.paramToAsk)[1:])
    tgt_user.save()
    return ast.literal_eval(tgt_user.paramToAsk)


# {'体育馆': ['体育馆名称‘, '体育场地'], 'datetimeV2': 0}
# {'体育馆': [{'体育馆名称': ['综体'], '体育场地': ['羽毛球馆']}], 'number': [2, 14, 8], 'datetimeV2': [{'type': 'datetime', 'values': [{'timex': 'XXXX-02-14T08', 'resolution': [{'value': '2022-02-14 08:00:00'}, {'value': '2023-02-14 08:00:00'}]}]}]}   