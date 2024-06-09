# data structures
import numpy as np
import pandas as pd

# visualization
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# dashboard
import streamlit as st

# others
import joblib

## load and modify dataset
df_base = pd.read_csv('../dataset/labeled_rfm.csv')
df_base['label'] = df_base['label'].astype(str)
names = df_base.select_dtypes(np.number).columns.drop('customer_id').tolist()

#### mapping labels
new_label = {
    '0': 'Whales', '1': 'New customers(1st)', 
    '2': 'New customers(2nd)', '3': 'One-time buyers'
}
df_base['new_label'] = df_base['label'].map(new_label)

#### 
x = df_base.groupby('new_label', observed=True)[names].mean()

## load model
scaler = joblib.load('../models/scaler.pkl')
kmeans = joblib.load('../models/kmeans.pkl')

### page title
st.title('Exploratory Data Analysis')

### histograms
col1, col2, col3 = st.columns(3)
with col1:
    fig_hist = px.histogram(data_frame=df_base, x=names[0], color='new_label', 
                            barmode='stack', opacity=0.7, 
                            color_discrete_sequence=[
                                px.colors.qualitative.Dark2[0], 
                                px.colors.qualitative.Dark2[1], 
                                px.colors.qualitative.Dark2[2], 
                                px.colors.qualitative.Dark2[3]
                            ],
                            width=500)
    
    fig_hist.update_layout(xaxis_title=names[0].title(), yaxis_title=None,
                           showlegend=False)

    st.plotly_chart(fig_hist, theme=None)

with col2:
    fig_hist = px.histogram(data_frame=df_base, x=names[1], color='new_label', 
                            barmode='stack', opacity=0.7,
                            color_discrete_sequence=[
                                px.colors.qualitative.Dark2[0], 
                                px.colors.qualitative.Dark2[1],
                                px.colors.qualitative.Dark2[2],
                                px.colors.qualitative.Dark2[3]
                            ],
                            width=500)
    
    fig_hist.update_layout(xaxis_title=names[1].title(), yaxis_title=None, 
                           showlegend=False)

    st.plotly_chart(fig_hist, theme=None)

with col3:
    fig_hist = px.histogram(data_frame=df_base, x=names[2], color='new_label', 
                            barmode='stack', opacity=0.7, 
                            color_discrete_sequence=[
                                px.colors.qualitative.Dark2[0],
                                px.colors.qualitative.Dark2[1],
                                px.colors.qualitative.Dark2[2],
                                px.colors.qualitative.Dark2[3]
                            ],
                            width=500)
    
    fig_hist.update_layout(xaxis_title=names[2].title(), yaxis_title=None, 
                           showlegend=False)

    st.plotly_chart(fig_hist, theme=None)

st.write(df_base[['recency', 'frequency', 'monetary']].describe().T)

### pie + bars
col4, col5 = st.columns([0.5, 0.5])

with col4:
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=df_base['new_label'].value_counts(ascending=True).index.tolist(), 
                         values=df_base['new_label'].value_counts(ascending=True).values, 
                         hole=0.5, marker={
                             'colors': [
                                 px.colors.qualitative.Dark2[0], 
                                 px.colors.qualitative.Dark2[2],
                                 px.colors.qualitative.Dark2[3], 
                                 px.colors.qualitative.Dark2[1]
                             ]
                         }))
    
    #### plot's size adjustment
    fig.update_layout(
        title={
            'text': '<b>Percentage(%) segmented customer account for</b>',
            'font': dict(size=27)
        },
        width=600, height=500)
    
    st.plotly_chart(fig, theme=None)

with col5:

    fig_bars = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                             subplot_titles=[
                                 'Recency', 'Monetary', 'Frequency'
                             ])
    for i, name in enumerate(names):
        fig_bars.add_trace(go.Bar(x=x.index.tolist(), y=x[name], 
                                  marker={
                                      'color': [
                                          px.colors.qualitative.Dark2[3], 
                                          px.colors.qualitative.Dark2[2], 
                                          px.colors.qualitative.Dark2[1], 
                                          px.colors.qualitative.Dark2[0]
                                      ]
                                  }, name=name), 
                           row=i+1, col=1)
        
    fig_bars.update_layout(showlegend=False,
                           title={
                               'text': '<b>Traits on \'\'RFM\'\' criteria</b>', 
                               'font': dict(size=27)},
                           width=700, height=500)

    st.plotly_chart(fig_bars, theme=None)

### stacked bars chart
country_segmetation = pd.crosstab(index=df_base['country'], columns=df_base['new_label'])
labels = country_segmetation.columns.tolist()

#### palette
palette = {
    'Whales': px.colors.qualitative.Dark2[0], 'New customers(1st)': px.colors.qualitative.Dark2[3],
    'New customers(2nd)': px.colors.qualitative.Dark2[2], 'One-time buyers': px.colors.qualitative.Dark2[1]
}

fig_stacked_bar = go.Figure()
for label in labels:
    fig_stacked_bar.add_trace(go.Bar(x=country_segmetation.index.tolist(), 
                                    y=country_segmetation[label],
                                    marker={
                                        'color': [
                                            palette[label]
                                        ]*len(country_segmetation.index.tolist())
                                    },
                                    name=label))
fig_stacked_bar.update_layout(
    barmode='stack', 
    title={
        'text': '<b>Distribution of customers in countries</b>',
        'font': dict(size=27)
    }
    )

st.plotly_chart(fig_stacked_bar, theme=None)