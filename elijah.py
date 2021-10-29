import sklearn
import streamlit as st
import pandas as pd
from sklearn import datasets
from datetime import datetime
import datetime as dt
import pydeck as pdk
import numpy as np



st.title("Geo-Data Streamlit Tutorial")

uber_files = ['/Users/elijahflomen/Downloads/archive/uber-raw-data-apr14.csv']

ubers_df = pd.DataFrame()
for file in uber_files:
    df = pd.read_csv(file,encoding='utf-8')
    ubers_df = pd.concat([df,ubers_df])

# Allow user to select frac of data to analyze
st.caption("Streamlit allows for the user to customize their EDAV experience")
user_frac=st.slider("fraction of data", min_value=0.0, max_value=1.0)
ubers_df = ubers_df.sample(frac=user_frac)    
ubers_df = ubers_df.drop(columns=['Base'])
ubers_df = ubers_df.rename(columns={"Lat": "lat", "Lon":"lon", "Date/Time": "Date"})

for i in ubers_df.index:
    df_date = ubers_df.at[i ,'Date'].split(" ",1)[0]
    ubers_df.at[i ,'Date'] = datetime.strptime(df_date, "%m/%d/%Y").date()
    ubers_df.at[i, 'Day'] = ubers_df.loc[i, 'Date'].strftime('%A')


st.subheader("Uber Pickups in NYC (April 2014)")
st.write(ubers_df)
col1, col2, col3 = st.columns(3)

user_cal_date = st.date_input("Select a specific day for pickups", value=dt.datetime(2014,4,1), 
    min_value=dt.datetime(2014,4,1), 
    max_value=dt.datetime(2014,4,30))

# Useful framework for data summaries
col1.metric("# of Trips", ubers_df.shape[0])
col2.metric("Mean Lat", round(ubers_df['lat'].mean(), 4))
col3.metric("Mean Lon", round(ubers_df['lon'].mean(), 4))

st.subheader("Map of Pickups From Calendar Date")
st.map(ubers_df.loc[ubers_df['Date'] == user_cal_date])

# Slider for categorical data with natural ordering...
st.subheader("Map of Pickups From A Given Day")
user_day_input = st.select_slider(label='Pick A Day', options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
st.map(ubers_df.loc[ubers_df['Day'] == user_day_input])


# Better visualizaiton for this type of dataset: 
st.subheader("Heat Map for Uber Pickups")
layers=[pdk.Layer(
    "HexagonLayer",
    data=ubers_df[["lon", "lat"]],
    get_position=["lon", "lat"],
    radius=100,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    ),]

initial_view_state={
    "latitude": ubers_df['lat'].mean(),
    "longitude": ubers_df['lon'].mean(),
    "zoom": 12,
    'pitch': 50}

st.pydeck_chart(pdk.Deck(map_style='light',layers=[layers], initial_view_state=initial_view_state))
        



