import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
	"""
	Question 모델

	Attributes:

	- question_text: 질문
	- pub_date: 질문 생성일
	"""
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		"""
		Question 모델의 출력 형식 정의

		Returns:
			- question_text 필드 값
		"""
		return self.question_text

	def was_published_recently(self):
		"""
		Question 모델의 최근 생성 여부 반환

		Returns:
			- 최근 생성 여부
		"""
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
	"""

	Choice 모델

	Attributes:

	- :class:`Question` question: 질문
	- choice_text: 선택지
	- votes: 투표수
	"""
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		"""
		Choice 모델의 출력 형식 정의

		Returns:
		- choice_text: 필드 값
		"""
		return self.choice_text
