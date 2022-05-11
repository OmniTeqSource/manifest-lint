FROM python:3.9

WORKDIR /app

COPY manifest_lint /app/manifest_lint
COPY pyproject.toml /app/pyproject.toml
RUN python -m pip install -U /app

ENTRYPOINT [ "python", "-m", "manifest_lint" ]