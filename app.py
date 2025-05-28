import os
import sys

import certifi
from dotenv import load_dotenv
ca= certifi.where()

load_dotenv()

mongoDBURL=os.getenv("MONGO_DB_ATLAS_URL")
port=os.getenv("PORT")

import pymongo
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from NetworkSecurity.utils.main_utils.utils import load_object
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from NetworkSecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME


client = pymongo.MongoClient(mongoDBURL, tlsCAFile=ca)

database= client[DATA_INGESTION_DATABASE_NAME]
collection= database[DATA_INGESTION_COLLECTION_NAME]

app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/",tags=["Authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train(request: Request):
    try:
        logging.info("Training pipeline started")
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return templates.TemplateResponse("train.html", {"request": request})

    except Exception as e:
        logging.error(f"Error in app.py: {e}")
        raise NetworkSecurityException(e, sys)   


@app.get("/predict",tags=["Prediction"])
async def predict(request: Request):
    try:
        logging.info("Prediction endpoint accessed")
        return templates.TemplateResponse("predict.html", {"request": request})
    except Exception as e:
        logging.error(f"Error in predict endpoint: {e}")
        raise NetworkSecurityException(e, sys)    

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('predict_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)
 

if __name__ == "__main__":
    try:
        logging.info("Starting the FastAPI application")
        app_run(app, host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        logging.error(f"Error starting FastAPI application: {e}")
        raise NetworkSecurityException(e, sys)