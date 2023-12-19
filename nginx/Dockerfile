FROM alpine:3.18.2

RUN apk update && apk upgrade && \
    apk add nginx openssl

RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 --nodes -days 365 \
		      -newkey rsa:2048 \
		      -keyout /etc/nginx/ssl/nginx.key \
		      -out /etc/nginx/ssl/nginx.crt \
		      -subj "/C=KR/ST=Seoul/O=42Seoul/OU-42Seoul/CN=yena.42.fr"

RUN mkdir -p /etc/nginx/http.d
COPY conf/nginx.conf /etc/nginx/http.d/

EXPOSE 443

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
