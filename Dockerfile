FROM python:3.8-slim-buster
COPY ./app /app
WORKDIR /app
RUN mkdir -p /app/dockerfiles
RUN apt-get -y update
RUN apt-get -y install gcc
RUN apt-get -y install g++
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install wheel
RUN python3 -m pip install gunicorn
RUN python3 -m pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8500", "wsgi:app"]
