from django.db import models


class Answer(models.Model):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_accepted', '-created_at']
