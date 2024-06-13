# dashboard
import streamlit as st

###
st.set_page_config(page_title='Customer Segmentation: Online Retail', 
                   layout='wide')
st.title('Overviews')
st.text(
    body='The power of data has gradually accepted for recent years in both traditional ways and modern ones.\
        \nBeside charts, we can now use machine learning to uncover hidden patters and help businesses unleash their potential.\
        \nThis dashboard will guide you through informations that machine learning model (KMeans) can find with 2 pages:'
)
st.markdown('##### 1. Exploratory Data Analysis\
            \n##### 2. Visualize Segmentation\
            \n#### Enjoys!')
st.markdown('*Creator: Le Gia Huy*')