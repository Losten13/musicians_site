FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR app

COPY . /app

RUN pip install -r requirements.txt


# CMD python manage.py makemigrations
# CMD python manage.py migrate
# CMD python manage.py runserver 0.0.0.0:8000

ENTRYPOINT ["./entrypoint.sh"]