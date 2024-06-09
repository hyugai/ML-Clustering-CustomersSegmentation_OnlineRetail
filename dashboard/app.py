# data structures
import numpy as np
import pandas as pd

# visualization
import plotly.express as px
import plotly.graph_objects as po

# dashboard
import streamlit as st

# others
import joblib

## load dataset
df_base = pd.read_csv('../dataset/labeled_rfm.csv')

## load model
scaler = joblib.load('../models/scaler.pkl')
kmeans = joblib.load('../models/kmeans.pkl')

