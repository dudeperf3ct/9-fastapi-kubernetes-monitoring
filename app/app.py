from fastapi import FastAPI

from app import classifier_router
from app.monitoring import instrumentator

app = FastAPI()
app.include_router(classifier_router.router)
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


@app.get("/")
async def root():
    return "Sentiment Classifier (0 -> Negative and 1 -> Positive)"


@app.get("/healthcheck", status_code=200)
async def healthcheck():
    return "dummy check! Classifier is all ready to go!"
