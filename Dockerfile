FROM python:3.11

RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
    gcc  \
    libpq-dev  \
    wait-for-it  \
    lsof  \
    && pip install --upgrade pip

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . /app
RUN poetry lock --no-update
RUN poetry install

CMD ["python", "main.py"]
