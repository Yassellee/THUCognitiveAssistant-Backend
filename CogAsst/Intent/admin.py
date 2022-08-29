from django.contrib import admin
from Intent import models


admin.site.register(models.Feature)
admin.site.register(models.Utterance)

class IntentAdmin(admin.ModelAdmin):
    list_display =['name', 'show_features']

admin.site.register(models.Intent, IntentAdmin)