from django.urls import path

from . import views  # 현재 패키지에서 views 모듈을 가져온다.

urlpatterns = [
    path("", views.index, name="index"),  # views.py에서 정의한 index 함수를 호출한다. 즉 views.index를 루트, 인덱스 페이지로 사용한다.
]
