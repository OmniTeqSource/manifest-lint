FROM python:3.9

RUN pip install -U pip pyyaml

WORKDIR /app

COPY manifest_lint /app/manifest_lint

ENTRYPOINT [ "python", "-m", "manifest_lint", ]