FROM python:3.7.5-buster

COPY ./requirements.txt /

RUN pip3 install -r requirements.txt

COPY ./ ./

CMD ["python", "./app.py"]