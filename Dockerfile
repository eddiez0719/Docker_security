FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd --create-home --uid 1001 appuser
COPY --from=builder /install /usr/local
COPY app.py .
USER appuser
EXPOSE 8080
ENV APP_ENV=unset
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]