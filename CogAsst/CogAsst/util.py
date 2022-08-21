from django.db import models
from Intent.models import *
from User.models import *
from Intent.utils import *
from User.utils import *
from strategy.LUIS_strategy import *
import codecs
import csv

# # query parameters that didn't matched and generate reply
# def askParam(tgt_user, paramToAsk, candidateParams, intent):
#     # print("askParam--")
#     # print(paramToAsk)
#     message = "以下哪一个是您想要在" + paramToAsk[0] + "中填入的参数？(如果没有，请在下面文字框中填入你想要填入的参数)"
#     return {"result": "dialogue", "intent": intent, "message": message, "candidateParams": candidateParams, "preparedParams":""}


# # failed to match intents
# def notFind(id):
#     update_state(id, 6)
#     return {"result": "failed", "intent": "", "message": "", "candidate": ['',''], "preparedParams":""}


# # provide potential intents list for user to choose from
# def askMatchedIntentList(matchedIntentList):
#     print('-------')
#     print(type(matchedIntentList))
#     message = "请选择您的意图"
#     return {"result": "dialogue", "intent": "暂时识别失败", "message": message, "candidateParams": [item for item in matchedIntentList], "preparedParams":""}



# # the state machine that controls the processing
# # state  meaning
# #   0    first recognization
# #   1    get the answer to querying potential intents list
# #   4    query parameters that didn't matched
# #   5    succeed
# def OnMessage(id, message):
#     tgt_user = User.objects.filter(username = id).first()
#     state = tgt_user.state
#     print(state)
#     if state == 0:
#         tgt_user.sentence = message
#         luis = LUIS(message)
#         luis.predict()
#         print(luis.recognize_intent())
#         tgt_user.intent = luis.recognize_intent()['top_intent']
#         tgt_user.matchedIntentList = luis.recognize_intent()['intents']
#         tgt_user.inputTokenize = luis.segment_sentence()
#         tgt_user.matchedEntity = luis.extract_entity()
#         tgt_user.save()
#         if tgt_user.intent is not None:  # 成功匹配
#             tgt_intent = Intent.objects.filter(name = tgt_user.intent).first()
#             paramToAsk = getParamToAsked(tgt_intent.entity, tgt_user.matchedEntity, tgt_user)  #list
#             if paramToAsked == []:  # 开始执行
#                 feedback = {"result": "finish", "intent": tgt_user.intent, "message": "", "candidate":['',''], "candidateParams":tgt_user.inputTokenize}
#                 update_state(id, 5)
#                 # addUtterance(id)
#             else:  # 询问参数
#                 feedback = askParam(tgt_user, paramToAsk, tgt_user.inputTokenize, tgt_user.intent)
#                 update_state(id, 4)
#         else:  # 匹配失败
#             askMatchedIntentList(tgt_user.matchedIntentList)
#             update_state(id, 1)
#     elif state == 1:
#         if message == "都不是":
#             feedback = notFind()
#             update_state(id, 0)
#         else:
#             tgt_intent = Intent.objects.filter(name = message).first()
#             paramToAsk = getParamToAsked(tgt_intent.entity, tgt_user.matchedEntity, tgt_user)  #list
#             if paramToAsked == []:  # 开始执行
#                 feedback = {"result": "finish", "intent": tgt_user.intent, "message": "", "candidate":['',''], "candidateParams":tgt_user.inputTokenize}
#                 update_state(id, 5)
#                 # addUtterance(id)
#             else:  # 询问参数
#                 feedback = askParam(tgt_user, paramToAsk, tgt_user.inputTokenize, tgt_user.intent)
#                 update_state(id, 4)
#     elif state == 4:
#         # TODO add
        # paramToAsk = get_paramToAsk(tgt_user, message)
#         if paramToAsk == []:  # 开始执行
#             feedback = {"result": "finish", "intent": tgt_user.intent, "message": "", "candidate":['',''], "candidateParams":tgt_user.inputTokenize}
#             update_state(id, 5)
#             # addUtterance(id)
#         else:  # 询问参数
#             feedback = askParam(tgt_user, paramToAsk, tgt_user.inputTokenize, tgt_user.intent)
#             update_state(id, 4)
#     elif state == 5:
#         feedback = {"result": "finish", "intent": tgt_user.intent, "message": "执行中", "candidate":['',''], "preparedParams":""}
#     else:
#         feedback = {"result": "eror", "intent": "", "message": "", "candidate":['',''],"preparedParams":""}
#     return feedback




def addIntent2db():
    with codecs.open('../intent2db.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            tgt_intent = Intent.objects.filter(name  = row['Name']).first()
            # if tgt_intent is None:
            print("none")
            intent_ = Intent.objects.create(name = row["Name"], entity = row["Entity"])
            features = ast.literal_eval(row["Features"])
            for key in list(features.keys()):
                Feature.objects.create(intent = intent_, feature_name = key, feature = str(features[key]))



def update_message(id, message):
    tgt_user = User.objects.filter(username = id).first()
    luis = LUIS(message)
    luis.predict()
    print(luis.recognize_intent())
    intentslist = luis.recognize_intent()
    inputTokenize = luis.segment_sentence()
    matchedEntity = luis.extract_entity()
    Process.objects.create(user = tgt_user, sentence = message, intentslist = intentslist, inputTokenize = inputTokenize, matchedEntity = matchedEntity)
    return intentslist


def getIntentParamList(intentparam):
    result = []
    intentparam = ast.literal_eval(intentparam)
    keys = list(intentparam.keys())
    for key in keys:
        if intentparam[key]!=0:
            result += intentparam[key]
        else:
            result.append(key)
    return result


def getMatchedEntityList(matchedEntity, intentParamList):
    # print(matchedEntity)
    # result = []
    # matchedEntity = ast.literal_eval(matchedEntity)
    # keys = list(matchedEntity.keys())
    # for i in range(0, len(intentParamList)):
    #     keyParam = intentParamList[i]
    #     for key in keys:
    #         if keyParam == "datetimeV2" and key == "datetimeV2":
    #             try:
    #                 result.append(matchedEntity['datetimeV2'][0]['values'][0]['timex'])
    #             except:
    #                 result.append(matchedEntity['datetimeV2'])
    #         elif key != 'datetimeV2':
    #             print(matchedEntity[key])
    #             print(matchedEntity[key][0].keys())
    #             for item in list(matchedEntity[key][0].keys()):
    #                 if item == keyParam:
    #                     result += (matchedEntity[key][0][item])
    #     if len(result) <  i+1:
    #         result.append('')
    # return result
    print(matchedEntity)
    result = []
    matchedEntity = ast.literal_eval(matchedEntity)
    keys = list(matchedEntity.keys())
    for i in range(0, len(intentParamList)):
        keyParam = intentParamList[i]
        for key in keys:
            if key == "datetimeV2":
                if keyParam == "datetimeV2":
                    result.append("datetimeV2")
            elif key == "number":
                if keyParam == "number":
                    result.append("number")         
            else:
                print(matchedEntity[key])
                print(matchedEntity[key][0].keys())
                for item in list(matchedEntity[key][0].keys()):
                    if item == keyParam:
                        result += keyParam
    return result
