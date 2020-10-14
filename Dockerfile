FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/src/app

CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000