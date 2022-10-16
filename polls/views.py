from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from django.contrib.auth.models import User

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


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
        question = get_object_or_404(Question, pk=kwargs["question_id"])
        if not question.can_vote():
            messages.error(request, "Voting is not allow")
            return redirect('polls:index')
        if not request.user.is_authenticated:
            messages.error(request, "Please login first")
            return redirect('login')
        select_vote = get_vote_for_user(question, request.user)
        return render(request, 'polls/detail.html', {'question': question, 'vote': select_vote})


class ResultsView(generic.DetailView):
    """Result view page"""
    model = Question
    template_name = 'polls/results.html'


def get_vote_for_user(question: Question, user: User):
    """Get vote for user in each question"""
    try:
        return Vote.objects.get(user=user, choice__question=question)
    except Vote.DoesNotExist:
        return None


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
        # selected_choice.votes += 1
        # selected_choice.save()
        select_vote = get_vote_for_user(question, request.user)
        if not get_vote_for_user(question, request.user):
            Vote.objects.create(user=request.user, choice=selected_choice)
        else:
            select_vote.choice = selected_choice
        select_vote.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
