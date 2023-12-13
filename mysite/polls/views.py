from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    polls 앱의 index 페이지를 반환한다.

    Args:
        request: 클라이언트로부터 받은 요청

    Returns:
        HttpResponse: index 페이지
    """
    return HttpResponse("Hello, world. You're at the polls index.")
