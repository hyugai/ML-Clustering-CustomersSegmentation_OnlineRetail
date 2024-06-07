# data structures
import numpy as np
import pandas as pd

# load model
import joblib

# dashboard
import streamlit as st
import altair as alt
import plotly.express as px

# load dataset
df_base = pd.read_csv('../dataset/rfm.csv')

# load models
scaler = joblib.load('../models/scaler.pkl')
kmeans = joblib.load('../models/4Clusters_model.pkl')


st.set_page_config(
    page_title='Online Retail', 
    layout='wide'
)
alt.themes.enable('dark')

with st.sidebar:
    st.title('Online Retail')

    seleted_mode = st.selectbox('Select a type of analysis', ['Exploratory Data Analysis', 'Customer Segmentation'])

if seleted_mode == 'Exploratory Data Analysis':
    st.write('hello world')

# segmentation
elif seleted_mode == 'Customer Segmentation':
    ###
    latest_date = st.date_input(
        label='The date since the last purchase'
    )
    min_date = pd.to_datetime('2010-12-01')
    recency = (pd.to_datetime(latest_date) - min_date).days

    ###
    frequency = st.number_input(
        label='Number of purchase', 
        min_value=1, 
        format='%d'
        )
    
    ###
    monetary = st.number_input(
        label='Total amount of spent money', 
        min_value=0., 
        format='%f'
    )