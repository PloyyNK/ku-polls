import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_date_same_with_pub_date(self):
        """
        current date/time is exactly the pub_date, the vote is still available
        """
        time = timezone.now()
        question = Question(pub_date=time)
        self.assertIs(question.can_vote(), True)

    def test_date_same_with_end_date(self):
        """
        current date/time is exactly the end date, the vote is still available
        """
        end = timezone.now()
        pub = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=pub, end_date=end)
        self.assertIs(question.can_vote(), True)

    def test_current_date_after_end_date(self):
        """Voting is not allow after end date"""
        end = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pub = timezone.now() - datetime.timedelta(days=3, seconds=3)
        question = Question(pub_date=pub, end_date=end)
        self.assertIs(question.can_vote(), False)

    def test_null_end_date(self):
        """Voting is always on if no end date"""
        pub = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=pub, end_date=None)
        self.assertIs(question.can_vote(), True)


def create_question(question_text, days):
    """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
