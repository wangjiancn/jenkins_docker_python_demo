FROM python:3.7.4-alpine



RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        python3-dev \
        pcre-dev \
        gcc \
        libc-dev \
        linux-headers \
        mariadb-dev \
    && pip install \
    --trusted-host=pypi.douban.com \
    -i http://pypi.douban.com/simple/ \
    --no-cache-dir \
    pipenv uwsgi

WORKDIR /app

COPY . /app

RUN pipenv install 
RUN apk del .build-deps

EXPOSE 5000

ENTRYPOINT [ "pipenv","run","blog/manage.py","runserver","0.0.0.0:5000" ]
