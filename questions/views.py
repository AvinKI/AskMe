from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Question , Like
from .forms import QuestionForm





@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()
            return redirect('question_detail', question.id)
    else:
        form = QuestionForm()
    return render(request, 'questions/ask_question.html', {'form': form})


@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    existing_like = Like.objects.filter(user=request.user, answer=answer)

    if existing_like.exists():
        existing_like.delete()
    else:
        Like.objects.create(user=request.user, answer=answer, is_like=True)

    return redirect('question_detail', pk=answer.question.id)


@login_required
def dislike_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    existing_dislike = Like.objects.filter(user=request.user, answer=answer)

    if existing_dislike.exists():
        existing_dislike.delete()
    else:
        Like.objects.create(user=request.user, answer=answer, is_like=False)

    return redirect('question_detail', pk=answer.question.id)


# question list

def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'questions/question_list.html', {'questions': questions})


# questions/views.py

from answers.forms import AnswerForm
from answers.models import Answer

from django.shortcuts import render, get_object_or_404
from .models import Question

from django.shortcuts import render, get_object_or_404
from .models import Question, Answer

from django.shortcuts import render, get_object_or_404
from .models import Question, Answer


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)

    # محاسبه تعداد لایک‌ها و دیسلایک‌ها
    like_count = question.like_set.filter(is_like=True).count()
    dislike_count = question.like_set.filter(is_like=False).count()

    # ارسال به قالب
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': answers,
        'like_count': like_count,
        'dislike_count': dislike_count
    })

# like

@login_required
@require_POST
def ajax_toggle_like(request):
    obj_type = request.POST.get('obj_type')
    obj_id = request.POST.get('obj_id')
    is_like = request.POST.get('is_like') == 'true'
    user = request.user

    if obj_type == 'question':
        obj = get_object_or_404(Question, pk=obj_id)
        like_obj, created = Like.objects.get_or_create(user=user, question=obj)
    elif obj_type == 'answer':
        obj = get_object_or_404(Answer, pk=obj_id)
        like_obj, created = Like.objects.get_or_create(user=user, answer=obj)
    else:
        return JsonResponse({'error': 'Invalid type'}, status=400)

    if not created and like_obj.is_like == is_like:
        like_obj.delete()
    else:
        like_obj.is_like = is_like
        like_obj.save()

    like_count = Like.objects.filter(**{obj_type: obj, 'is_like': True}).count()
    dislike_count = Like.objects.filter(**{obj_type: obj, 'is_like': False}).count()

    return JsonResponse({'like_count': like_count, 'dislike_count': dislike_count})

