FROM alpine:latest
MAINTAINER Jacob Elias
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 443
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["app.py"]
