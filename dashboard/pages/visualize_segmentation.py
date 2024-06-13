# data structures
import numpy as np
import pandas as pd

# visualization
import plotly.express as px
import plotly.graph_objects as go

# dashboard
import streamlit as st

# others
import joblib

## load dataset
df_base = pd.read_csv('../dataset/labeled_rfm.csv')
df_base['label'] = df_base['label'].astype(str)

### map new label
new_labels = {
    '0': 'Whales', '1': 'New customers(2nd)',
    '2': 'One-time buyers', '3': 'New customers(1st)'
}

df_base['mapped_label'] = df_base['label'].map(new_labels)

### map size
sizes = ((df_base['mapped_label'].value_counts() / len(df_base))*50).to_dict()
df_base['mapped_size'] = df_base['mapped_label'].map(sizes)

## load model
scaler = joblib.load('../models/scaler.pkl')
kmeans = joblib.load('../models/kmeans.pkl')


###
st.title('Visualize segmentation')

mode = st.radio(label='Select a type of information to fill', 
                options=['Customer\'s ID', 'RFM info'])

col1, col2 = st.columns([0.17, 0.6])

fig_scatter = px.scatter_3d(
    data_frame=df_base, 
    x='recency', y='frequency', z='monetary',
    size='mapped_size',
    color='mapped_label', 
    color_discrete_sequence=[
        px.colors.qualitative.Dark2[0],
        px.colors.qualitative.Dark2[3],
        px.colors.qualitative.Dark2[2],
        px.colors.qualitative.Dark2[1]
    ],
    opacity=0.55,
    width=1000, height=800
)
fig_scatter.update_traces(
    marker={
        'line': dict(width=0)
    }
)


if mode == 'RFM info':
    with col1:
        ####
        date = st.date_input(
            label='***Date of the latest successful order***', 
            min_value=pd.to_datetime('2010-12-01'),
            max_value=pd.to_datetime('2011-12-09')
        )
        recency = (pd.to_datetime(date) - pd.to_datetime('2010-12-01')).days

        ####
        frequency = st.number_input(
            label='***Number of orders***',
            format='%d',
            min_value=1
        )

        ####
        monetary = st.number_input(
            label='***Amount of spent money***',
            format='%f',
            min_value=0.01
        )

    fig_scatter.add_trace(
        go.Scatter3d(
            name='Your customer',
            x=[recency], y=[frequency], z=[monetary], 
            mode='markers+text',
            text='Your customer\'s here!', textfont={
                'color': px.colors.qualitative.Light24[5],
                'size': 20
            },
            marker={
                'symbol': 'diamond',
                'color': px.colors.qualitative.Light24[5],
                'size': 8.5
            }
        )
    )
    st.plotly_chart(fig_scatter, theme=None)
        

elif mode == 'Customer\'s ID':
    with col1:
        try:
            #### get the ID of the customer
            id = st.number_input(
                label='Enter customer\'s ID here',
                format='%d', 
                min_value=12347, 
                max_value=18287
            )

            #### retrive RFM infomation
            mask_id = df_base['customer_id'] == id
            selected_customer = df_base[mask_id]

            ####
            recency = selected_customer['recency'].values[0]
            frequency = selected_customer['frequency'].values[0]
            monetary = selected_customer['monetary'].values[0]

            #### type of the customer
            button = st.button(
                label='Click to know the type of this customer'
            )
            label = selected_customer['mapped_label'].values[0]
            if button:
                if label == 'Whales':
                    st.success(label)
                elif label == 'New customers(2nd)':
                    st.warning(label)
                elif label == 'New customers(1st)':
                    st.info(label)
                else:
                    st.warning(label)

        except:
            st.error('Please check the ID again!')

    ####
    fig_scatter.add_trace(
        go.Scatter3d(
            name='Your customer',
            x=[recency], y=[frequency], z=[monetary], 
            mode='markers+text', 
            text='Your customers\'s here!', 
            textfont={
                'color': px.colors.qualitative.Light24[5],
                'size': 20
            }, 
            marker={
                'symbol': 'diamond', 
                'color': px.colors.qualitative.Light24[5],
                'size': 8.5
            }
        )
    )
    st.plotly_chart(fig_scatter, theme=None)