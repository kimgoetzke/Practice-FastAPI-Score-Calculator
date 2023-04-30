# syntax=docker/dockerfile:1

FROM python:3.11.2-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

COPY ./main.py ./__init__.py ./alembic.ini /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]