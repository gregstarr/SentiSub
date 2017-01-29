from django.db import models

# Create your models here.

class SubReddit(models.Model):
    subreddit_name = models.CharField(max_length=20)
    subscribers = models.IntegerField(null=True)
    positivity_index = models.IntegerField(null=True)
    negativity_index = models.IntegerField(null=True)
    neutrality_index = models.IntegerField(null=True)
    num_positive_comments = models.IntegerField(null=True)
    num_negative_comments = models.IntegerField(null=True)
    num_neutral_comments = models.IntegerField(null=True)

    def __str__(self):
        return self.subreddit_name
