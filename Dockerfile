FROM python:3.7-slim-buster

WORKDIR /home/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python app.py