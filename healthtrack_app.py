"""HealthTrack — minimal demo API used in the Week 3 security pipeline demo.

Deliberately small and dependency-light so the live demo (hadolint, Trivy,
Bandit, GitHub Actions) stays fast and easy to follow in class.
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(service="healthtrack", status="ok")


@app.get("/healthz")
def healthz():
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    # Binding to all interfaces is required so the process is reachable
    # from outside the container; the container/network boundary is the
    # real security control here. Bandit flags this as B104 by default —
    # reviewed and explicitly accepted below, not blindly silenced.
    app.run(host="0.0.0.0", port=8080)  # nosec B104