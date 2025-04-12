from django.conf import settings
from tags.models import Tag
from answers.models import Answer
from django.db import models
from django.contrib.auth import get_user_model


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()

    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_like = models.BooleanField()

    def __str__(self):
        return f"{'Like' if self.is_like else 'Dislike'} by {self.user.username}"
