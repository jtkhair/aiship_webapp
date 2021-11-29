"""
Web server script that exposes endpoints and pushes ship principal parameter data (csv file) to Redis for passenger
ship powering by model server. Polls Redis for response from model server.

Deployment is based on pretrained model developed using scikit learn
"""

# %%
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from io import StringIO
import logging
# import pandas as pd
import pickle
# from sklearn.preprocessing import MinMaxScaler

# scaler = MinMaxScaler()

# %%

# app configuration
app = FastAPI(title="Passenger Ship Powering Prediction",
              description="API for passenger ship powering prediction using Deep Learning")

# css folder
app.mount(
    "/style",
    StaticFiles(directory="src/static"),
    name="static")

# mount jinja template
templates = Jinja2Templates(directory="src/templates")

# Log setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename="logs.log")

# load model/scaler
# model = pickle.load(open("../model/mlp_pwr_best_model.sav", 'rb'))
# scaler = pickle.load(open("../model/scaler_pwr.sav", 'rb'))

# home page
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    sliders = [
        "LWL",
        "B",
        "T",
        "L/B",
        "B/T",
        "Disp",
        "CB",
        "VS",
        "Fn"
    ]

    return templates.TemplateResponse("home.html", 
        {
            "request": request,
            "sliders": sliders
        })

@app.post("/predict/", response_class=HTMLResponse)
async def predict(
    request: Request,
    LWL: float = Form(...),
    B: float = Form(...),
    T: float = Form(...),
    LB: float = Form(...),
    BT: float = Form(...),
    Disp: float = Form(...),
    CB: float = Form(...),
    VSmin: float = Form(...),
    VSmax: float = Form(...)):
    # Fn: float = Form(...)):
    sliders = [
        {"name":"LWL","val":LWL},
        {"name":"B","val": B},
        {"name":"T","val": T},
        {"name":"L/B","val": LB},
        {"name":"B/T","val":BT},
        {"name":"Disp","val":Disp},
        {"name":"CB","val":CB}
        # {"name":"VS","val":VS},
        # {"name":"Fn","val":Fn}
    ]
    return templates.TemplateResponse("prediction.html", 
        {
            "request": request,
            "sliders": sliders
        })