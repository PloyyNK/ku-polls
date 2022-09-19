from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question, Vote


def index(request):
    """
    Display all questions in order of publication date

    Returns:
        HttpResponseObject -- index page
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
        Display details of selected question

        Returns:
            HttpResponseObject -- detail page
        """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Voting is not available")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """
        Display result of selected question

        Returns:
            HttpResponseObject -- result page
        """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view page"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Check if the question is available to vote"""
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if not question.can_vote():
            messages.error(request, "Voting is not allow")
            return redirect('polls:index')
        if not request.user.is_authenticated:
            messages.error(request, "Please login first")
            return redirect('login')
        return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    """Result view page"""
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """
    Display the vote result of selected questions.

        Returns:
        HttpResponseObject -- vote page
        """
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            user_vote = Vote.objects.get(user=user)
            user_vote.choice = selected_choice
            user_vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(choice=selected_choice, user=user).save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
