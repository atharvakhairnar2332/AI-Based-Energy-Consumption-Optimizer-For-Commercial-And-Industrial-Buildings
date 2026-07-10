from fastapi import FastAPI
from fastapi import UploadFile, File, Form, HTTPException
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

from local_pipeline import (
    load_lstm_resources,
    load_ppo_resources,
    validate_dataset,
    predict_future_environment,
    predict_fan_decision
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app = FastAPI(
    title="AI Energy Consumption Optimizer API",
    version="1.0.0"
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

@app.on_event("startup")
def startup():

    load_lstm_resources()

    load_ppo_resources()


@app.get("/")
def home():

    return {

        "status": "Backend Running",

        "message": "LSTM + PPO Models Loaded"

    }

@app.post("/predict")
def predict(
    file: UploadFile = File(...),
    occupancy: int = Form(...)
):
    
   file_path = os.path.join(
    UPLOAD_FOLDER,
    file.filename
)
   with open(file_path, "wb") as buffer:

     shutil.copyfileobj(
        file.file,
        buffer
    )

   try:

     df = validate_dataset(file_path)
     future_environment = predict_future_environment(df)
     decision = predict_fan_decision(
     future_environment,
     occupancy
)

     return {

        "status": "success",

        "future_environment": future_environment,

        "decision": decision

    }
   
   except Exception as e:

    raise HTTPException(

        status_code=400,

        detail=str(e)

    )
   
   finally:

        if os.path.exists(file_path):

            os.remove(file_path)