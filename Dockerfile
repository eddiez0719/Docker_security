# Stage 1: build — installs deps into an isolated prefix/dir, nothing else
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: runtime — only the installed packages + app code ship here
FROM python:3.11-slim
WORKDIR /app

# Create a non-root user to run the app as
RUN useradd --create-home --uid 1001 appuser

COPY --from=builder /install /usr/local
COPY healthtrack_app.py .

# Numeric UID (DL3066): a name may not resolve on every host/orchestrator.
USER 1001
EXPOSE 8080
# Exec form (DL3025): no shell, and a urlopen exception already exits non-zero.
HEALTHCHECK --interval=30s --timeout=3s \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "healthtrack_app:app"]