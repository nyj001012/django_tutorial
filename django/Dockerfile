FROM python:3.9.6-alpine

# 파이썬을 실행할 때 버퍼링되지 않고 표준 출력(1)과 표준 에러(2)의 스트림을 더 빠르게 보여주는 환경 변수
ENV PYTHONUNBUFFERED 1

# apk 업데이트
RUN apk add --update --no-cache

# vim 설치
RUN apk add vim

# /app/django/ 디렉토리 생성
RUN mkdir -p /app/django

# 현재 디렉토리의 파일들을 컨테이너의 /app/django/ 폴더에 추가
COPY . /app/django

# 작업 디렉토리를 /app/django_tutorial/ 로 변경
WORKDIR /app/django

# 파이썬 가상환경 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# 유저 생성
RUN adduser -D yena

# 소유자 변경
RUN chown -R yena:yena /app/django

# 권한 변경
RUN chmod -R 755 /app/django

# 유저 변경
USER yena

# 8000번 포트 개방
EXPOSE 8000

# 컨테이너에서 실행할 명령
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
