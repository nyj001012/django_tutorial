from deprecated import deprecated
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic  # F() 사용: F() 객체를 이용하여 race condition을 방지한다.
from django.db.models import F
from django.utils import timezone
from .models import Question, Choice


class IndexView(generic.ListView):
	"""
	Question 모델의 최근 5개 질문을 보여주는 뷰

	Attributes:
		template_name: 템플릿 파일의 경로
		context_object_name: 템플릿 파일에서 사용할 컨텍스트 변수의 이름
	"""
	template_name = "polls/index.html"
	context_object_name = "latest_question_list" # 템플릿 파일에서 사용할 컨텍스트 변수의 이름

	def get_queryset(self):
		"""
		최근 5개의 질문을 반환한다.

		Returns:
			QuerySet: 최근 5개의 질문
		"""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
	"""
	Question 모델의 상세 페이지를 보여주는 뷰

	Attributes:
		model: 사용할 모델
		template_name: 템플릿 파일의 경로
	"""
	model = Question
	template_name = "polls/detail.html"

	def get_queryset(self):
		"""
		미래의 pub_date를 가진 질문은 제외한다.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	"""
	Question 모델의 결과 페이지를 보여주는 뷰

	Attributes:
		model: 사용할 모델
		template_name: 템플릿 파일의 경로
	"""
	model = Question
	template_name = "polls/results.html"


@deprecated("제너릭 뷰를 사용한다.")
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


@deprecated("제너릭 뷰를 사용한다.")
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


@deprecated("제너릭 뷰를 사용한다.")
def results(request, question_id):
	"""
	question_id에 해당하는 질문의 결과 페이지를 반환한다.

	Args:
		request (HttpRequest): 클라이언트로부터 받은 요청
		question_id (int): 질문의 id

	Returns:
		HttpResponse: question_id에 해당하는 질문의 결과 페이지
	"""
	question = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
	"""
	question_id에 해당하는 질문에 투표한다.

	Args:
		request (HttpRequest): 클라이언트로부터 받은 요청
		question_id (int): 질문의 id

	Returns:
		HttpResponse: question_id에 해당하는 질문에 투표하는 페이지
	"""
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST["choice"])
	# F() 예제 1: selected_choice.filter(pk=request.POST["choice"]).update(votes=F("votes") + 1)
	except (KeyError, Choice.DoesNotExist):
		return render(
			request,
			"polls/detail.html",
			{
				"question": question,
				"error_message": "You didn't select a choice.",
			},
		)
	else:
		selected_choice.votes = F("votes") + 1  # F() 예제 2
		selected_choice.save()
		# POST 데이터를 정상적으로 처리한 후에는 항상 HttpResponseRedirect를 반환해야 한다.
		# 이렇게 하면 사용자가 브라우저의 "뒤로" 버튼을 눌렀을 때 데이터가 두 번 저장되는 것을 방지할 수 있다.
		return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
