"""app-service — minimal demo API for the multi-environment deploy exercise.

The pipeline builds ONE image and promotes the SAME image through
dev -> qa -> uat -> preprod -> prod. Nothing about the image changes between
stages; only the APP_ENV environment variable (injected at deploy time, not
baked in at build time) changes, so this endpoint can prove which
environment a given running container actually landed in.
"""
import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        service="app-service",
        environment=os.environ.get("APP_ENV", "unset"),
        status="ok",
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    # 0.0.0.0 is required so the process is reachable from outside the
    # container; the real security boundary is the container/network layer,
    # not this bind address. Reviewed and explicitly accepted, not silenced.
    app.run(host="0.0.0.0", port=8080)  # nosec B104
