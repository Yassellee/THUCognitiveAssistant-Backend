# from time import timezone
from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.username

# class matchedEntity(models.Model):
#     matchedEntity = models.TextField(max_length=300, default="")
#     user = models.ForeignKey(User, related_name='user_matchedEntity', on_delete=models.CASCADE)

class Process(models.Model):
    user = models.ForeignKey(User, related_name='process_user', on_delete=models.CASCADE) 
    sentence = models.CharField(max_length=20, default="", blank = True)
    # state = models.IntegerField(default=0)
    intent = models.CharField(max_length=20, default="", blank = True)
    intentslist = models.CharField(max_length=300, default="", blank = True)
    inputTokenize = models.TextField(max_length=300, default="", blank = True)
    matchedEntity = models.TextField(max_length=300, default="", blank = True)
    endTime = models.DateTimeField(default = timezone.now, blank = True)
    startTime = models.DateTimeField(auto_now_add = True)
    # paramToAsk = models.TextField(max_length=300, default="", blank = True)

    def __str__(self):
        return self.user.username

    def show_logs(self):
        query_logs = self.log_process.all()
        print(query_logs)
        res = [i.message for i in query_logs]
        return query_logs
    show_logs.short_description = 'logs'

# TODO log  defaultParam
class Log(models.Model):
    process = models.ForeignKey(Process, related_name='log_process', on_delete=models.CASCADE)
    message = models.TextField(max_length=300, default="", blank = True)
    type = models.IntegerField(blank = True, default = 0)

    def __str__(self):
        return self.process.sentence

    def sentence(self):
        return self.process.sentence



# TODO 差一个互相确认的机制