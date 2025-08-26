from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import QuizQuestion
import random

def index_view(request):
    return render(request, 'quiz/index.html')

def learn_more_view(request):
    return render(request, 'quiz/learn_more.html')

def quiz_view(request):
    """
    Displays a random quiz question, avoiding the last seen question.
    If the request is from HTMX, it returns only the quiz container part.
    """
    last_question_id = request.session.get('last_question_id')
    
    # Wyklucz ostatnie pytanie z losowania, jeśli to możliwe
    question_ids = QuizQuestion.objects.exclude(id=last_question_id).values_list('id', flat=True)

    # Jeśli po wykluczeniu nie ma pytań (np. jest tylko jedno w bazie), losuj ze wszystkich
    if not question_ids:
        question_ids = QuizQuestion.objects.values_list('id', flat=True)

    if not question_ids:
        context = {'error': 'Brak pytań w bazie.'}
        return render(request, 'quiz/quiz_page.html', context)

    random_id = random.choice(list(question_ids))
    question = get_object_or_404(QuizQuestion, id=random_id)
    
    # Zapisz ID bieżącego pytania w sesji na potrzeby następnego żądania
    request.session['last_question_id'] = question.id

    links = [question.real_url, question.phishing_url_1, question.phishing_url_2]
    random.shuffle(links)

    context = {
        'question_id': question.id,
        'links': links
    }
    
    # If the request is from HTMX (e.g., "Next Question" button), 
    # render only the partial template to swap.
    if request.htmx:
        return render(request, 'quiz/partials/quiz_content.html', context)

    return render(request, 'quiz/quiz_page.html', context)

@require_POST
def check_answer_view(request):
    """
    Checks the user's answer submitted via HTMX.
    Returns an HTML fragment with the result.
    """
    selected_link = request.POST.get('selected_link')
    question_id = request.POST.get('question_id')

    if not selected_link or not question_id:
        return HttpResponseBadRequest("Brak wymaganych danych: 'selected_link' lub 'question_id'.")

    question = get_object_or_404(QuizQuestion, id=question_id)
    is_correct = (selected_link == question.real_url)

    context = {
        'is_correct': is_correct,
        'correct_answer': question.real_url
    }
    return render(request, 'quiz/partials/result.html', context)
