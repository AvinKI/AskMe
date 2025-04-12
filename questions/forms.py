from django import forms
from .models import Question
from tags.models import Tag


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your question title'}),
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Describe your question in detail...', 'rows': 5}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
