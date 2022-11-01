from django.contrib import admin
from User import models


class ProcessAdmin(admin.ModelAdmin):
    list_display =['user', 'startTime', 'endTime', 'sentence','intent','intentslist','matchedEntity','show_logs']
    list_filter = ['user']
    readonly_fields = ('startTime','endTime')

class LogAdmin(admin.ModelAdmin):
    list_display =['process','process_id','sentence','message', 'type']
    fields = ['process','message', 'type']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','process_num','show_score']
    

admin.site.register(models.Process, ProcessAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Log, LogAdmin)