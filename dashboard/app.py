# data structures
# %%
import numpy as np
import pandas as pd

# visualization
import plotly.express as px
import plotly.graph_objects as go

# load model
import joblib

# dashboard
import streamlit as st
import altair as alt
import plotly.express as px

# others
import datetime

# load dataset
df_base = pd.read_csv('../dataset/labeled_rfm.csv')
df_base['label'] = df_base['label'].astype(str)

new_label = {'0': 'Whales', '2': 'New customers (2nd)', '1': 'One-time buyers', '3': 'New cutomers (1st)'}
df_base['Segmentation\'s type'] = df_base['label'].map(new_label)


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
    col1, col2 = st.columns(2)

    with col1:
        ###
        latest_date = st.date_input(
            label='The date since the last purchase', 
            min_value=pd.to_datetime('2010-12-01')
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

    with col2:
        if st.button('Make prediction'):
            st.write('Testing')

    fig = px.scatter_3d(data_frame=df_base, x='recency', y='frequency', z='monetary', 
                        color='Segmentation\'s type',
                        color_discrete_sequence=[
                            px.colors.qualitative.Pastel1[0],
                            px.colors.qualitative.Pastel[1],
                            px.colors.qualitative.Pastel1[2],
                            px.colors.qualitative.Pastel1[3]
                        ], 
                        opacity=0.55)
    fig.add_trace(go.Scatter3d(x=[50], y=[100], z=[500], name='Customer',
                               mode='markers+text', 
                               text='<b>Your customer here!</b>', textfont=dict(color=px.colors.qualitative.Light24[0], size=20, style='italic'),
                               marker=go.scatter3d.Marker(color=px.colors.qualitative.D3[3], size=10.5, symbol='diamond')))
   
    st.plotly_chart(fig, theme=None)