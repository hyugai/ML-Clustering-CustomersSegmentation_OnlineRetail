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


st.set_page_config(
    page_title='Online Retail', 
    layout='wide'
)
alt.themes.enable('dark')

with st.sidebar:
    st.title('Online Retail')

    selected_analysis_type = st.selectbox('Select a type of analysis', ['Exploratory Data Analysis', 'Customer Segmentation'])