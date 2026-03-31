from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

from backend.database import init_db, save_prediction, get_history
from backend.logic import predict_purchase

app = FastAPI(title="Real Estate Purchasing Decision System")

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Mount frontend directory for static files
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

class PredictionRequest(BaseModel):
    price: float
    location: str
    size: float
    income: float
    amenities: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = os.path.join(frontend_dir, "index.html")
    with open(index_path, "r") as f:
        return f.read()

@app.post("/api/predict")
async def formulate_prediction(req: PredictionRequest):
    result = predict_purchase(
        price=req.price,
        location=req.location,
        size=req.size,
        income=req.income,
        amenities=req.amenities
    )
    
    # Save to history
    save_prediction(
        price=req.price,
        location=req.location,
        size=req.size,
        income=req.income,
        amenities=req.amenities,
        likelihood=result["likelihood"],
        probability=result["probability"]
    )
    
    return result

@app.get("/api/history")
async def get_prediction_history():
    return get_history()
