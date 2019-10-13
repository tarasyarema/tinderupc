FROM python:3.7

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "-w", "4", "server:app"]
