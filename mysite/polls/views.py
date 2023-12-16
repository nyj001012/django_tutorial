from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.template import loader
from .models import Question


def index(request):
	"""
	polls 앱의 index 페이지를 반환한다.

	Args:
		request: 클라이언트로부터 받은 요청

	Returns:
		HttpResponse: index 페이지
	"""
	latest_question_list = Question.objects.order_by("-pub_date")[:5]
	template = loader.get_template("polls/index.html")
	context = {
		"latest_question_list": latest_question_list,
	}
	return HttpResponse(template.render(context, request))


def detail(request, question_id):
	"""
	question_id에 해당하는 질문의 상세 페이지를 반환한다.

	Args:
		request (HttpRequest): 클라이언트로부터 받은 요청
		question_id (int): 질문의 id

	Returns:
		HttpResponse: question_id에 해당하는 질문의 상세 페이지
	"""
	question = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
	"""
	question_id에 해당하는 질문의 결과 페이지를 반환한다.

	Args:
		request (HttpRequest): 클라이언트로부터 받은 요청
		question_id (int): 질문의 id

	Returns:
		HttpResponse: question_id에 해당하는 질문의 결과 페이지
	"""
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)


def vote(request, question_id):
	"""
	question_id에 해당하는 질문에 투표한다.

	Args:
		request (HttpRequest): 클라이언트로부터 받은 요청
		question_id (int): 질문의 id

	Returns:
		HttpResponse: question_id에 해당하는 질문에 투표하는 페이지
	"""
	return HttpResponse("You're voting on question %s." % question_id)
