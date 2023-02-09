FROM python:3.11 as builder

WORKDIR /build

COPY . .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN --mount=source=.git,target=.git,type=bind \
    pip install --upgrade .

FROM python:3.11

RUN addgroup --system --gid 1001 lintuser
RUN adduser --system --uid 1001 lintuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN chown -R lintuser:lintuser /app
RUN chmod 755 /app

USER lintuser
