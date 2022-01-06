from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from app.sentiment.model import SentimentBertModel

router = APIRouter()


@router.post("/classify")
async def predict_sentiment(input_text: str = Query(..., min_length=2)):
    classifier = SentimentBertModel("distilbert-base-uncased-finetuned-sst-2-english")
    out_dict = classifier.predict(input_text)
    return JSONResponse(out_dict)
