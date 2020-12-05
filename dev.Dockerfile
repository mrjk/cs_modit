# dev.Dockerfile

# --- builder
FROM python:3.8.1-buster AS builder
RUN apt-get update && apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip


# --- builder-venv
FROM builder AS builder-venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt


# --- tester
FROM builder-venv AS tester

ENV FLASK_APP=app
ENV FLASK_ENV=development

COPY . /app
WORKDIR /app
#RUN /venv/bin/pytest


# --- runner
FROM martinheinz/python-3.8.1-buster-tools:latest AS runner
COPY --from=tester /venv /venv
COPY --from=tester /app /app

WORKDIR /app
EXPOSE 4000/tcp

VOLUME /app/etc /app/var
# /venv/bin/flask run --port 4000 --host 0.0.0.0
ENTRYPOINT ["/venv/bin/flask", "run", "--host", "0.0.0.0", "--port", "4000"]
#ENTRYPOINT ["/venv/bin/python3", "-m", "blueprint"]
USER 1001

LABEL name={NAME}
LABEL version={VERSION}
