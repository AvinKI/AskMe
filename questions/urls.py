from django.urls import path
from .views import *

urlpatterns = [
    path('ask/', ask_question, name='ask_question'),
    path('', question_list, name='question_list'),
    path('<int:pk>/', question_detail, name='question_detail'),

    path('ajax-toggle/', ajax_toggle_like, name='ajax_toggle_like'),

]
