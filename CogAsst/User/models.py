from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, default="")

# class matchedEntity(models.Model):
#     matchedEntity = models.TextField(max_length=300, default="")
#     user = models.ForeignKey(User, related_name='user_matchedEntity', on_delete=models.CASCADE)

class Process(models.Model):
    user = models.ForeignKey(User, related_name='process_user', on_delete=models.CASCADE) 
    sentence = models.CharField(max_length=20, default="", blank = True)
    # state = models.IntegerField(default=0)
    intent = models.CharField(max_length=20, default="", blank = True)
    intentslist = models.CharField(max_length=20, default="", blank = True)
    inputTokenize = models.TextField(max_length=300, default="", blank = True)
    matchedEntity = models.TextField(max_length=300, default="", blank = True)
    # paramToAsk = models.TextField(max_length=300, default="", blank = True)

# TODO log  defaultParam