from typing import Any
from django import http
from django.http.response import HttpResponse
from django.template import loader
from django.http import Http404
from .models import Question
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, QuestionUser
from polls.models import Question
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .decorators import Timer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from .models import Question
from django.shortcuts import render, get_object_or_404, redirect
def is_superuser(user):
    return user.is_superuser


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
        

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Verificar si la pregunta está habilitada
        if not self.object.enabled:
            disabled_date = self.object.enabled_date.strftime('%Y-%m-%d %H:%M:%S') if self.object.enabled_date else "Desconocida"
            disabled_message = f"Esta encuesta fue deshabilitada el día {disabled_date}."
            context = {
                'question': self.object,
                'disabled_message': disabled_message,
            }
            return self.render_to_response(context)

        # Resto de la lógica de la vista para permitir a los usuarios votar
        # ...

        context = {
            'question': self.object,
        }
        return self.render_to_response(context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
@Timer(max_votes=1, minutes=5)
def index(request):
    questions = Question.objects.all()
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    # Recupera la última pregunta contestada
    latest_question_user = QuestionUser.objects.all().last()
    
    context = {
        'latest_question_list': latest_question_list,
        'latest_question_user': latest_question_user,
        'questions': questions,  # Agrega todas las preguntas al contexto
    }
    
    return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {
        'question': question,
    })

@login_required
@Timer(max_votes=1, minutes=5)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    
    # Verificar si el usuario ya ha votado en esta pregunta
    if QuestionUser.objects.filter(user=user, question=question).exists():
        return render(request, 'polls/votado.html', {'question': question})

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No seleccionaste una opción válida.",
        })
    else:
        # Registra el voto en la tabla QuestionUser
        QuestionUser.objects.create(user=user, question=question, choice=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
#Ver los votos realizados
def voted_users(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question_users = QuestionUser.objects.filter(question=question)

    return render(request, 'polls/voted_users.html', {'question': question, 'question_users': question_users})


@login_required
def unvote_and_revote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    # Verificar si el usuario ya ha votado en esta pregunta
    existing_vote = QuestionUser.objects.filter(user=user, question=question).first()
    if existing_vote:
        # Elimina el voto existente
        existing_vote.choice.votes -= 1
        existing_vote.choice.save()
        existing_vote.delete()

    # Redirige al usuario a la página de detalles de la pregunta para votar nuevamente
    return redirect('polls:detail', question_id=question_id)




@user_passes_test(is_superuser)
def disable_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if question.enabled:
        question.enabled = False
        question.enabled_date = timezone.now()
        question.save()

    return redirect('http://127.0.0.1:8000/')

@user_passes_test(is_superuser)
def enable_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not question.enabled:
        question.enabled = True
        question.enabled_date = None
        question.save()

    return redirect('http://127.0.0.1:8000/')