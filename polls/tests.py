import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Question, Choice


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


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
            If no questions exist, an appropriate message is displayed.
            """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
            Questions with a pub_date in the past are displayed on the
            index page.
            """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
            Questions with a pub_date in the future aren't displayed on
            the index page.
            """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
            Even if both past and future questions exist, only past questions
            are displayed.
            """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
            The questions index page may display multiple questions.
            """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def setUp(self):
        # superclass setUp creates a Client object and initializes test database
        super().setUp()
        self.username = "testuser1"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Tester1"
        self.user1.set_password("FatChance!")
        self.user1.save()

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        self.client.login(username=self.username, password=self.password)
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class UserAuthTest(TestCase):

    def setUp(self):
        # superclass setUp creates a Client object and initializes test database
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Tester"
        self.user1.set_password("FatChance!")
        self.user1.save()
        # we need a poll question to test voting
        q = create_question("Test q", days=-1)
        q.save()
        # a few choices
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_login_view(self):
        """a user can login using the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using a POST request
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser",
                     "password": "FatChance!"
                     }
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))

