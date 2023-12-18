import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
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


def create_question(question_text, days):
	"""
	주어진 question_text와 days로 Question을 생성한다.
	과거에 작성한 질문은 음수, 미래에 작성한 질문은 양수로 days를 받는다.

	Args:
		days: pub_date에 더할 날 수
		question_text: 질문 내용

	Returns:
		Question: 생성된 Question 객체
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
	"""
	Question 모델의 DetailView 테스트
	"""

	def test_future_question(self):
		"""
		미래에 작성된 question의 detail view는 404 not found를 반환해야 한다.
		"""
		future_question = create_question(question_text="Future question.", days=5)
		url = reverse("polls:detail", args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		"""
		과거에 작성된 question의 detail view는 question_text를 반환해야 한다.
		"""
		past_question = create_question(question_text="Past Question.", days=-5)
		url = reverse("polls:detail", args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)
