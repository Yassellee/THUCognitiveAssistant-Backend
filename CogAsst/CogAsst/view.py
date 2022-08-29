from inspect import isdatadescriptor
from socket import BTPROTO_RFCOMM
from ssl import OP_NO_COMPRESSION
from strategy.LUIS_strategy import *
from utils.LUIS_editor import *
from CogAsst.util  import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
from strategy.LUIS_strategy import *


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
        username = request.POST.get("username")
        message = request.POST.get("message")
        intentlist = update_message(username, message)
        print(intentlist)
        print(type(intentlist))
        data = str({"intents": intentlist})
        return JsonResponse({
            'code': 200,
            'data': data
        }, status=200)
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
        intent = request.POST.get("intent")
        username = request.POST.get("username")
        tgt_user = User.objects.filter(username = username).first()
        process = tgt_user.process_user.last()
        process.intent = intent
        process.save()
        intentParam = Intent.objects.filter(name = intent).first().entity
        intentParamList = getIntentParamList(intentParam)
        return JsonResponse({
            'code': 200,
            'data': [intentParamList, getMatchedEntityList(process.matchedEntity, intentParamList)]
        }, status=200)
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
        process = tgt_user.process_user.last()
        return JsonResponse({
            'code': 200,
            'data': {"inputTokenize": process.inputTokenize}
        }, status=200)
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
        failedParam =  add_Param(request)
        if failedParam == []:
            return JsonResponse({
                'code': 200,
                'data': "success"
            }, status=200)
        else:
            return JsonResponse({
                'code': 200,
                'data': {"failedParam": failedParam}
            }, status=200)
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


@csrf_exempt
def add_utterance(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        tgt_user = User.objects.filter(username = username).first()
        process = tgt_user.process_user.last()
        print(process.intent)
        intentParam = Intent.objects.filter(name = process.intent).first().entity
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
                        return JsonResponse({
                            'code': 400,
                            'data': childParam + 'is not matched'
                        }, status=400
                        )
        luis_editor = LUIS_editor()
        luis_editor.add_example_utterance(labeled_example_utterance)
        Utterance.objects.create(intent = Intent.objects.filter(name = process.intent).first(), utterance = labeled_example_utterance)
        no_add = 0
        for utterance in reversed(Utterance.objects.all()):
            if utterance.isAdd == 0:
                no_add += 1
                if no_add == 5:  # TODO add this to configratiion file
                    luis_editor.train_app()
                    luis_editor.publish_app()
                    print('train')
                    for utterance in reversed(Utterance.objects.all()):
                        utterance.isAdd = 1
                        utterance.save()
                        no_add -= 1
                        if no_add == 0:
                            break
            else:
                break
        return JsonResponse({
            'code': 200,
            'data': "success",
        }, status=200
        )
    else:
        return JsonResponse({
            'code': 400,
            'data': "method error"
        }, status=400
        )
