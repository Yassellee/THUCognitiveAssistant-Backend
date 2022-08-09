from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', view.index),
    # path('result_web/', view.result_web),
    # path('result/', view.result),
    path('get_intentlist/', view.get_intentlist),
    path('get_intentParam/', view.get_intentParam)

]
