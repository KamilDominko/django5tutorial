from django.test import TestCase

import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() ma zwracać Fałsz dla pytań których pub_date jest w przyszłości."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_pubised_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() ma zwracać False dla pytań których pub_date jest starsze od 1 dnia"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_pubised_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() ma zwracać True dla pytań których pub_date jest w przeciągu ostatniego dnia."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_pubised_recently(), True)


def create_question(question_text: str, days: int) -> Question:
    """Tworzy pytanie z podanym `question_text` i datą o `days` przesuniętą
    od teraz (ujemne `days` dla pytań z przeszłości i dodatnie `days` dla pytań z przyszłości).

    Args:
        question_text (str): tekst pytania
        days (int): ilość dni

    Returns:
        Question: pytanie
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """Jeżeli nie ma żadnych pytań to powinno wyświetlić o tym informacje."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Pytania z `pub_date` w przeszłosci powinny być wyświetlane na stronie index'u."""
        question = create_question("Past question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        """Pytania z `pub_date` w przyszłosci nie powinny się wyświetlać."""
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Jeżeli są dwa pytania: jedno z przeszłości i jedno z przyszłości, to tylko
        pytanie z przeszłości powinno być wyświetlone.
        """
        question = create_question("Past question", -30)
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self):
        """Strona index'u powinna wyświetlać wiele pytań."""
        question1 = create_question("Past question 1", -30)
        question2 = create_question("Past question 2", -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question2, question1]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """Widok szczegółów dla pytania z `pub_date` w przyszłości powinien zwrócić 404 - nie znaleziono"""
        future_question = create_question("Future question", 5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("Past Question", -5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsView(TestCase):
    def test_future_question(self):
        future_question = create_question("Future question", 20)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
