from django.db import models

class Intent(models.Model):
    name = models.CharField(max_length=20, default="", verbose_name="intent name")
    user = models.CharField(max_length=20, default="no user", verbose_name="intent user")
    entity = models.TextField(max_length=300, default="")
    

class Feature(models.Model):
    feature_name = models.CharField(max_length=20, default="", verbose_name="feature_name")
    intent = models.ForeignKey(Intent, related_name='feature_intent', on_delete=models.CASCADE)


class FeatureContent(models.Model):
    feature = models.ForeignKey(Feature, related_name='feature', on_delete=models.CASCADE)
    feature_content = models.CharField(max_length=20, default="", verbose_name="feature_content")


# 表述积累