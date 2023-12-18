import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
	"""
	Question 모델 테스트
	"""

	def test_was_published_recently_with_future_question(self):
		"""
		미래의 pub_date를 가진 Question 모델은 was_published_recently() 메서드가 False를 반환해야 한다.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		1일보다 오래된 pub_date를 가진 Question 모델은 was_published_recently() 메서드가 False를 반환해야 한다.
		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		1일 이내의 pub_date를 가진 Question 모델은 was_published_recently() 메서드가 True를 반환해야 한다.
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)