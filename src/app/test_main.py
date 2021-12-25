"""
Script to test pretrained model deployed in the webapp and inferencing process
"""

# import libraries & dependencies

from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from io import StringIO
import logging
import matplotlib.pyplot as plt
import pandas as pd
import pickle

# load model/scaler
model = pickle.load(open("src/model/mlp_pwr_best_model.sav", 'rb'))
scaler = pickle.load(open("src/model/scaler_pwr.sav", 'rb'))

# load data
df = pd.read_csv('/code/aiship_webapp/src/data/INPUT_80.csv').round(2)

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
df_predicted_P = pd.DataFrame(predicted_P, index=y.index)
df_predicted_P.columns = ['LWL', 'B', 'T', 'L/B', 'B/T', 'Disp', 'CB', 'Vs', 'Fn', 'P']

# merge scaled P to input file
df['P'] = df_predicted_P['P']
df_output = df.round(2)

# Output table
output_table = df_output.values.tolist()
output_header = df.columns

# Visualize result
plt.plot(df_predicted_P['Fn'],df_predicted_P['P'], marker ='o')
plt.title('Power VS Froude number')
plt.xlabel('Fn')
plt.ylabel('Power, kW')
plt.savefig('/results/OUTPUT_INPUT_80_Pred.png', bbox_inches='tight')

plt.show()
