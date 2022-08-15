from django.db import models
from Intent.models import *
from User.models import *
from Intent.utils import *
from User.utils import *
from strategy.LUIS_strategy import *

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