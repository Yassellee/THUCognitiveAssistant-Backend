from strategy.LUIS_strategy import *
from utils.LUIS_editor import *
from CogAsst.util  import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
from strategy.LUIS_strategy import *
import time


@csrf_exempt
def index(request):
    context = {}
    context['sentence'] = 'test sentence'
    return render(request, 'index.html', context)


# @csrf_exempt
# def result_web(request):
#     print(request.POST)
#     userid = request.POST.get("userid")
#     context = OnMessage(userid, request.POST.get("sentence"))
#     context['id'] = userid
#     return render(request, 'result.html', context)

# @csrf_exempt
# def result(request):
#     print(request.POST)
#     userid = request.POST.get("userid")
#     context = OnMessage(userid, request.POST.get("sentence"))
#     context['id'] = userid
#     return JsonResponse({
#         'code': 200,
#         'data': context
#     }, status=200)

@csrf_exempt
def get_intentlist(request):
    """ post username and sentence, return with potential intents list

    Returns
        As the result of recognize_intent() is not JSON serializable, it is turn into string first
        {
            "code": 200,
            "data": "{'intents': {'top_intent': '体育馆预约', 'intents': {'体育馆预约': <azure.cognitiveservices.language.luis.runtime.models._models_py3.Intent object at 0x000001E9B2172E80>}}}"
        }
    """
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            message = request.POST.get("message")
            intentlist, process = update_message(username, message)
            print(intentlist)
            print(type(intentlist))
            data = str({"intents": intentlist})
            gen_sendlog('get_intentlist', request, process)
            return gen_response(200, data, process)
        except:
            return JsonResponse({
                'code': 400,
                'data': "post error"
            }, status=400)
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400)


@csrf_exempt
def get_intentParam(request):
    """ post username and intent, return intentParam and matchedEntity

    Returns
        {
            "code": 200,
            "data": {
                "intentParam": "{'体育馆': ['体育馆名称', '体育场地'], 'datetimeV2': 0}",
                "matchedEntity": "{'体育馆': [{'体育馆名称': ['综体'], '体育场地': ['羽毛球馆']}], 'datetimeV2': [{'type': 'date', 'values': [{'timex': '2022-08-10', 'resolution': [{'value': '2022-08-10'}]}]}]}"
            }
        }
    """
    if request.method == 'POST':
        try:
            intent = request.POST.get("intent")
            username = request.POST.get("username")
            tgt_user = User.objects.filter(username = username).first()
            if tgt_user == None:
                return JsonResponse({
                    'code': 400,
                    'data': "user does not exist"
                }, status=400)
            process = tgt_user.process_user.last()
            process.intent = intent
            process.save()
            gen_sendlog('get_intentParam', request, process)
            try:
                intentParam = Intent.objects.filter(name = intent).first().entity
            except:
                return gen_response(400,"intent does not exist", process)
            print(intentParam)
            intentParamList = getIntentParamList(intentParam)
            data = [intentParamList, getMatchedEntityList(process.matchedEntity, intentParamList)]
            return gen_response(200,data,process)
        except:
            return JsonResponse({
                'code': 400,
                'data': "post error"
            }, status=400)
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400)


@csrf_exempt
def get_inputTokenize(request):
    """

    Returns
        {
            "code": 200,
            "data": {
                "inputTokenize": "['我', '要', '预约', '明天', '综', '体', '的', '羽毛', '羽毛球', '羽毛球馆', '球馆']"
            }
        }
    """
    if request.method == 'GET':
        username = request.GET.get("username")
        print(username)
        tgt_user = User.objects.filter(username = username).first()
        if tgt_user == None:
                return JsonResponse({
                    'code': 400,
                    'data': "user does not exist"
                }, status=400)
        process = tgt_user.process_user.last()
        gen_sendlog('get_inputTokenize', request, process)
        data = {"inputTokenize": process.inputTokenize}
        return gen_response(200, data, process)
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400)


@csrf_exempt
def add_params(request):
    """ add params and return the failed params' name

    Returns
        success:
        {
            "code": 200,
            "data": "success"
        }
        failed:
        {
            "code": 200,
            "data": {
                "failedParam": [
                    "体育馆"
                ]
            }
        }
    """
    if request.method == 'POST':
        try: 
            failedParam, process =  add_Param(request)
            gen_sendlog('add_params', request, process)
            if failedParam == []:
                return gen_response(200, "success", process)
            else:
                return gen_response(200, {"failedParam": failedParam}, process)
        except:
            return JsonResponse({
                'code': 400,
                'data': "post error"
            }, status=400
            )
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400
        )


@csrf_exempt
def init(request):
    # print('yes')
    addIntent2db()
    return JsonResponse({
        'code': 200,
        'data': "succss"
    }, status=200)


@limit_decor(60)
def run_add_utterance(labeled_example_utterance:str,train):
    try:
        print(train)
        print('in add')
        luis_editor = LUIS_editor()
        print(labeled_example_utterance)
        luis_editor.add_example_utterance(ast.literal_eval(labeled_example_utterance))
        print('added')
        if train:
            print('train pre')
            luis_editor.train_app()
            luis_editor.publish_app()
            print('train')
    except Exception:
        return -1



@csrf_exempt
def add_utterance(request):
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            tgt_user = User.objects.filter(username = username).first()
            if tgt_user == None:
                return JsonResponse({
                    'code': 400,
                    'data': "user does not exist"
                }, status=400)
            process = tgt_user.process_user.last()
            gen_sendlog('add_utterance', request, process)
            print(process.intent)
            try:
                intentParam = Intent.objects.filter(name = process.intent).first().entity
            except:
                return gen_response(400,"intent does not exist", process)
            intentParam = ast.literal_eval(intentParam)
            matchedParam = process.matchedEntity
            matchedParam = ast.literal_eval(matchedParam)
            labeled_example_utterance = {}
            labeled_example_utterance['text'] = process.sentence
            labeled_example_utterance['intentName'] = process.intent
            labeled_example_utterance['entityLabels'] = []
            for i in range(len(list(intentParam.keys()))):
                param = list(intentParam.keys())[i]
                if intentParam[param] != 0:
                    labeled_example_utterance['entityLabels'].append({})
                    labeled_example_utterance['entityLabels'][i]['startCharIndex'] = 0
                    labeled_example_utterance['entityLabels'][i]['endCharIndex'] = len(process.sentence)-1
                    labeled_example_utterance['entityLabels'][i]['entityName'] = param
                    labeled_example_utterance['entityLabels'][i]['children'] = []
                    for childParam in intentParam[param]:
                        if childParam in matchedParam.keys():
                            labeled_example_utterance['entityLabels'][i]['children'].append({
                                "startCharIndex": matchedParam[childParam]['startIndex'],
                                "endCharIndex": matchedParam[childParam]['endIndex'],
                                "entityName": childParam,
                            })
                        else:
                            return gen_response(400, childParam + 'is not matched', process)
            Utterance.objects.create(intent = Intent.objects.filter(name = process.intent).first(), utterance = labeled_example_utterance)
            no_add = 0
            train = False
            for utterance in reversed(Utterance.objects.all()):
                if utterance.isAdd == 0:
                    no_add += 1
                    if no_add == 5:  # TODO add this to configratiion file
                        train = True
                        print('tttt')
                        for utterance in reversed(Utterance.objects.all()):
                            utterance.isAdd = 1
                            utterance.save()
                            no_add -= 1
                            if no_add == 0:
                                break
                else:
                    break
            t1 = MyThread(target=run_add_utterance, args=(str(labeled_example_utterance),train))
            t1.start()
            # t1.join()
            result = t1.get_result()
            if result == -1:
                return gen_response(400, "thread error", process)
            return gen_response(200, "success", process)
        except:
            return JsonResponse({
                'code': 400,
                'data': "post error"
            }, status=400
            )
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400
        )


@csrf_exempt
def get_matchedParamInfo(request):
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            tgt_user = User.objects.filter(username = username).first()
            if tgt_user == None:
                return JsonResponse({
                    'code': 400,
                    'data': "user does not exist"
                }, status=400)
            process = tgt_user.process_user.last()
            gen_sendlog('get_matchedParam', request, process)
            intent = process.intent
            try:
                intentParam = Intent.objects.filter(name = intent).first().entity
            except:
                return gen_response(400, "intent does not exist", process)
            intentParamList = getIntentParamList(intentParam)
            print('hi')
            return gen_response(200, [intentParamList, getMatchedEntityInfo(process.matchedEntity, intentParamList)], process)
        except:
            return JsonResponse({
                'code': 400,
                'data': "post error"
            }, status=400
            )
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400)