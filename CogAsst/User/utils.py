from sqlite3 import paramstyle
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


def add_Param(request):
    position = ast.literal_eval(request.POST.get("position"))
    content = ast.literal_eval(request.POST.get("content"))
    username = request.POST.get("username")
    tgt_user = User.objects.filter(username = username).first()
    process = tgt_user.process_user.last()
    matchedEntity = ast.literal_eval(process.matchedEntity)
    print(process.intent)
    paramRequired = Intent.objects.filter(name = process.intent).first().entity
    paramRequired = ast.literal_eval(paramRequired)
    keys = list(paramRequired.keys())
    for key in keys:
        for paramName in list(content.keys()):
            if paramRequired[key] != 0:
                if paramName in paramRequired[key] :
                    if key not in matchedEntity:
                        matchedEntity[key] = {}
                    matchedEntity[key]['text'] = content[paramName]
                    matchedEntity[key]['startIndex'] = position[paramName][0]
                    matchedEntity[key]['endIndex'] = position[paramName][1]
                    content[paramName] = True
            else:
                if paramName == key:
                    matchedEntity[key] = {}
                    matchedEntity[key]['text'] = content[paramName]
                    matchedEntity[key]['startIndex'] = position[paramName][0]
                    matchedEntity[key]['endIndex'] = position[paramName][1]
                    content[paramName] = True
    process.matchedEntity = matchedEntity
    process.save()
    failedParam = []
    for item in content:
        if content[item] is not True:
            failedParam.append(item)
    return failedParam




# {'体育馆': ['体育馆名称‘, '体育场地'], 'datetimeV2': 0}
# {'体育馆': [{'体育馆名称': ['综体'], '体育场地': ['羽毛球馆']}], 'number': [2, 14, 8], 'datetimeV2': [{'type': 'datetime', 'values': [{'timex': 'XXXX-02-14T08', 'resolution': [{'value': '2022-02-14 08:00:00'}, {'value': '2023-02-14 08:00:00'}]}]}]}   