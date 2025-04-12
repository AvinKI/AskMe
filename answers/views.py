from django.shortcuts import render, get_object_or_404, redirect
from questions.models import Question
from answers.forms import AnswerForm
from answers.models import Answer
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
@require_POST
@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question

    if request.user != question.user:
        return redirect('question_detail', pk=question.pk)

    question.answers.filter(is_accepted=True).update(is_accepted=False)

    answer.is_accepted = True
    answer.save()

    return redirect('question_detail', pk=question.pk)
