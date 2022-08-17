from ssl import OP_NO_COMPRESSION
from strategy.LUIS_strategy import *
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
    print('yes')
    addIntent2db()
    return JsonResponse({
        'code': 200,
        'data': "succss"
    }, status=200)
