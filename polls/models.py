import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """Question text, publication date, and end date for questions"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, default=None)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """True if question question is published recently"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """True of the question is now published"""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """True if user can vote on this question"""
        if self.end_date is None:
            return self.pub_date <= timezone.now()
        return self.pub_date <= timezone.now() <= self.end_date

    def __str__(self):
        """Return question with text of question"""
        return self.question_text


class Choice(models.Model):
    """Text of choice"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """Total vote"""
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return text of choice"""
        return self.choice_text


class Vote(models.Model):
    """Model for voting"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def __str__(self):
        return f"user={self.user}, question={self.choice.question}, choice={self.choice.choice_text}"
