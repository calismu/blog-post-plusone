FROM python:3.12-bullseye

EXPOSE 8000

WORKDIR /app

RUN apt-get update
RUN apt-get install build-essential pkg-config libpq-dev postgresql -y

COPY ./api/source/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./api/source/oneplus .

CMD ["gunicorn", "oneplus.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=1", "--max-requests=1", "--timeout=100", "--log-level=debug"]
