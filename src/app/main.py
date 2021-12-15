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
import pandas as pd
import pickle


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
model = pickle.load(open("src/model/mlp_pwr_best_model.sav", 'rb'))
scaler = pickle.load(open("src/model/scaler_pwr.sav", 'rb'))

# home page
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    graph_data1 = [['Speed', 'Power'],
          [10,  0],
          [15,  0],
          [20,  0],
          [25,  0],
          [30,  0]]

    graph_data2 = [['Fn', 'Power'],
          [0.10,  0],
          [0.20,  0],
          [0.30,  0],
          [0.40,  0],
          [0.50,  0]]

    return templates.TemplateResponse("home.html", 
        {
            "request": request,
            "graph_data1": graph_data1,
            "graph_data2": graph_data2,
        })

@app.post("/predict/", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
   
    # only accept csv
    if file.filename.split(".")[-1] != "csv":
        return {"error": "undefined file extension"}
    else:
        # return byte
        raw_data = await file.read()

        # byte to str
        str_data = str(raw_data,'utf-8')

        # prepare string as input for pandas
        prep_data = StringIO(str_data)

        # create df
        df = pd.read_csv(prep_data).round(2)

        # html table
        input_table = df.values.tolist()
        input_header = df.columns

        # Preprocess data
        data_scaled = scaler.transform(df.drop(['ID'],1))
        df_data_scaled = pd.DataFrame(data_scaled, index=df.index)
        df_data_scaled.columns = ['LWL', 'B', 'T', 'L/B', 'B/T', 'Disp', 'CB', 'Vs', 'Fn', 'P']

        #  Create label
        y = df_data_scaled.drop(['P'], 1)

        # Infer powering
        predict_P = model.predict(y)

        # merge predicted_P to df
        df_predict_P = y
        df_predict_P['P'] = predict_P.tolist()

        # inverse scale
        predicted_P = scaler.inverse_transform(df_predict_P)
        df_predicted_P = pd.DataFrame(predicted_P, index=X.index)
        df_predicted_P.columns = ['LWL', 'B', 'T', 'L/B', 'B/T', 'Disp', 'CB', 'Vs', 'Fn', 'P']

        # merge scaled P to input file
        df['P'] = df_predicted_P['P']
        df_output = df.round(2)

        # Output table
        output_table = df_output.values.tolist()
        output_header = df.columns

        # sample graph
        graph_data1 = df_output[['Vs', 'P']].values.tolist()
        graph_data1.insert(0, ['Vs', 'Predicted P'])

        graph_data2 = df_output[['Fn', 'P']].values.tolist()
        graph_data2.insert(0, ['Fn', 'Predicted P'])
    
    return templates.TemplateResponse("prediction.html", 
        {
            "request": request,
            "output_table": output_table,
            "output_header": output_header,
            "graph_data1": graph_data1,
            "graph_data2": graph_data2,
        })
