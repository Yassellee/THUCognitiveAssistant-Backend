from django.db import models
from Intent.models import *
from User.models import *
from Intent.utils import *
from User.utils import *
from configuration import Config
import codecs
import csv
import time
import threading
from django.http import JsonResponse
from django.utils import timezone


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


def get_cogSt(message):
    config = Config()    
    if config.cognitive_strategy == "LUIS":
        from strategy.LUIS_strategy import LUIS
        return LUIS(message)
    


def addIntent2db():
    with codecs.open('../intent2db.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            tgt_intent = Intent.objects.filter(name  = row['Name']).first()
            if tgt_intent :
                print('yes')
                tgt_intent.delete()
            tgt_intent = Intent.objects.create(name = row["Name"], entity = row["Entity"])
            features = ast.literal_eval(row["Features"])
            for key in list(features.keys()):
                Feature.objects.create(intent = tgt_intent, feature_name = key, feature = str(features[key]))



def update_message(id, message):
    tgt_user = User.objects.filter(username = id).first()
    if tgt_user == None:
        tgt_user = User.objects.create(username = id)
    cogSt = get_cogSt(message)
    cogSt.predict()
    print(cogSt.recognize_intent())
    intentslist = cogSt.recognize_intent()
    inputTokenize = cogSt.segment_sentence()
    matchedEntity = cogSt.extract_entity()
    process = Process.objects.create(user = tgt_user, sentence = message, intentslist = intentslist, inputTokenize = inputTokenize, matchedEntity = matchedEntity)
    return intentslist, process


def getIntentParamList(intentparam):
    result = []
    # print(intentparam)
    intentparam = ast.literal_eval(intentparam)
    keys = list(intentparam.keys())
    # print(intentparam)
    # print(keys)
    for key in keys:
        if intentparam[key]!=0:
            if intentparam[key] != []:
                result += (intentparam[key])
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
    # for i in range(0, len(intentParamList)):
    #     keyParam = intentParamList[i]
    #     for key in keys:
    #         result.append()
    return keys


def getMatchedEntityInfo(matchedEntity, intentParamList):
    print(matchedEntity)
    result = []
    matchedEntity = ast.literal_eval(matchedEntity)
    keys = list(matchedEntity.keys())
    for i in range(0, len(intentParamList)):
        keyParam = intentParamList[i]
        for key in keys:
            if key == keyParam:
                if keyParam == "datetimeV2" :
                    try:
                        result.append(matchedEntity['datetimeV2'][0]['values'][0]['timex'])
                    except:
                        result.append(matchedEntity['datetimeV2']['text'])
                elif keyParam == "personName" or keyParam == "phoneNumber":
                    try:
                        result.append(matchedEntity[keyParam][0])
                    except:
                        result.append(matchedEntity[keyParam]['text'])
                elif keyParam == "money" :
                    try:
                        result.append(str(matchedEntity['money'][0]['number']))
                    except:
                        result.append(str(matchedEntity['money']['text']))
                else:
                    result.append(matchedEntity[key]['text'])
        if len(result) <  i+1:
            result.append('')
    print(result)
    return result
    for i in range(0, len(intentParamList)):
        keyParam = intentParamList[i]
        for key in keys:
            result.append()
    return keys


class MyThread(threading.Thread):
    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.func = target
        self.args = args
        self.result = None

    def run(self):
        # 接受返回值
        # print(*self.args)
        self.result = self.func(*self.args)

    def get_result(self):
        # 线程不结束,返回值为None
        try:
            return self.result
        except Exception:
            return None


# 为了限制真实请求时间或函数执行时间的装饰器
def limit_decor(limit_time):
    """
    :param limit_time: 设置最大允许执行时长,单位:秒
    :return: 未超时返回被装饰函数返回值,超时则返回 None
    """

    def functions(func):
        # 执行操作
        def run(*params):
            this_func = MyThread(target=func, args=params)
            # 主线程结束(超出时长),则线程方法结束
            this_func.setDaemon(True)
            this_func.start()
            # 计算分段沉睡次数
            sleep_num = int(limit_time // 1)
            sleep_nums = round(limit_time % 1, 1)
            # 多次短暂沉睡并尝试获取返回值
            for i in range(sleep_num):
                time.sleep(1)
                info = this_func.get_result()
                if info is not None:
                    return info
            time.sleep(sleep_nums)
            # 最终返回值(不论线程是否已结束)
            if this_func.get_result() is not None:
                return this_func.get_result()
            else:
                return -1  # 超时返回  可以自定义

        return run

    return functions


def gen_response(code, data, pro):
    print(timezone.now())
    pro.endTime = timezone.now()
    pro.save()
    Log.objects.create(process = pro, message = str({'code': code, 'data': data}), type = 1)
    return JsonResponse({
            'code': code,
            'data': data
        }, status=code)


def gen_sendlog(interface, request,pro):
    pro.endTime = timezone.now()
    pro.save()
    data={}
    if 'username' in request.POST:
        data['username'] = request.POST.get("username")
    if 'intent' in request.POST:
        data['intent'] = request.POST.get("intent")
    if 'message' in request.POST:
        data['message'] = request.POST.get("message")
    if 'position' in request.POST:
        data['position'] = request.POST.get("position")
    if 'content' in request.POST:
        data['content'] = request.POST.get("content")
    Log.objects.create(process = pro, message = str({'interface':interface, 'data':data}), type = 2)