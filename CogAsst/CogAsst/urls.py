from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', view.index),
    # path('result_web/', view.result_web),
    # path('result/', view.result),
    path('get_intentlist/', view.get_intentlist),
    path('get_intentParam/', view.get_intentParam),
    path('get_inputTokenize', view.get_inputTokenize),
    path('add_params/', view.add_params),
    path('init', view.init)
]