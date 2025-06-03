FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    libpq-dev

WORKDIR /opt
COPY poetry.lock pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi

COPY . .

FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq5 && \
    groupadd -r wwwgroup && \
    useradd -r -g wwwgroup -d /opt www && \
    chown -R www:wwwgroup /opt

WORKDIR /opt
COPY --from=builder --chown=www:wwwgroup /opt/.venv /opt/.venv
COPY --from=builder --chown=www:wwwgroup /opt /opt

ENV PATH="/opt/.venv/bin:$PATH"
USER www
EXPOSE 8000
