from django.test import TestCase

import datetime
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() zwraca Fałsz dla pytań których pub_date jest w przuszłości"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_pubised_recently(), False)
