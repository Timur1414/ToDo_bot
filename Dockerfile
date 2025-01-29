FROM python:3.12
LABEL authors="timat"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y

COPY . /workdir
WORKDIR /workdir

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
