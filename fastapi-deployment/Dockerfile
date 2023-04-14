FROM python:3.9.16-slim

WORKDIR /app

RUN set -ex \
    && apt-get -y update \
    && apt-get -y install curl \
    && pip install poetry

COPY pyproject.toml poetry.lock download_model.sh ./ 

RUN set -ex \
    & poetry install --no-dev

ARG MODEL_ARCHIVE_LINK

RUN ./download_model.sh $MODEL_ARCHIVE_LINK

COPY . .

CMD ["poetry", "run", "python", "serve_with_monitoring.py"]