from django.contrib import admin
from User import models


class ProcessAdmin(admin.ModelAdmin):
    list_display =['user', 'startTime', 'endTime', 'sentence','intent','intentslist','matchedEntity','show_logs']
    list_filter = ['user']
    readonly_fields = ('startTime','endTime')

class LogAdmin(admin.ModelAdmin):
    list_display =['process','sentence','message', 'type']
    fields = ['process','message', 'type']

admin.site.register(models.Process, ProcessAdmin)
admin.site.register(models.User)
admin.site.register(models.Log, LogAdmin)