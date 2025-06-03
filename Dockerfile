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
    groupadd -r appgroup && \
    useradd -r -g appgroup -d /opt appuser && \
    chown -R appuser:appgroup /opt

WORKDIR /opt
COPY --from=builder --chown=appuser:appgroup /opt/.venv /opt/.venv
COPY --from=builder --chown=appuser:appgroup /opt /opt

ENV PATH="/opt/.venv/bin:$PATH"
USER appuser
EXPOSE 8000
