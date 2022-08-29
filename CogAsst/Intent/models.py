from email.policy import default
from django.db import models

class Intent(models.Model):
    name = models.CharField(max_length=20, default="", verbose_name="intent name")
    user = models.CharField(max_length=20, default="no user", verbose_name="intent user")
    entity = models.TextField(max_length=300, default="")
    def show_features(self):
        query_features = self.feature_intent.all()
        print(query_features)
        res = [i.feature_name for i in query_features]
        return res
    show_features.short_description = 'intent'

class Feature(models.Model):
    feature_name = models.CharField(max_length=20, default="", verbose_name="feature_name")
    intent = models.ForeignKey(Intent, related_name='feature_intent', on_delete=models.CASCADE)
    feature = models.TextField(max_length=300, default="")

class Utterance(models.Model):
    intent = models.ForeignKey(Intent, related_name='utterance_intent', on_delete=models.CASCADE)
    isAdd = models.IntegerField(default = 0)
    utterance = models.TextField(max_length=300, default="")


# 表述积累
# 学习