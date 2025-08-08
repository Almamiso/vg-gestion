import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.api.v1.router import api_router

# Configure JSON logging
logger = logging.getLogger()
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

app = FastAPI(title="VG Backend")

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

app.include_router(api_router, prefix="/api/v1")