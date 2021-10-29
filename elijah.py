import sklearn
import streamlit as st
import pandas as pd
from sklearn import datasets
from datetime import datetime
import datetime as dt
import pydeck as pdk
import numpy as np



st.title("Geo-Data Dataset Tutorial")

uber_files = ['/Users/elijahflomen/Downloads/archive/uber-raw-data-apr14.csv']

ubers_df = pd.DataFrame()
for file in uber_files:
    df = pd.read_csv(file,encoding='utf-8')
    ubers_df = pd.concat([df,ubers_df])

# Only take 40% of the data to speed up visualization
ubers_df = ubers_df.sample(frac=0.1)    
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

# st.subheader("Heat Map for UK Accidents")

# UK_ACCIDENTS_DATA = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'

# layer = pdk.Layer(
#     'HexagonLayer', 
#     UK_ACCIDENTS_DATA,
#     get_position=['lng', 'lat'],
#     auto_highlight=True,
#     elevation_scale=50,
#     pickable=True,
#     elevation_range=[0, 3000],
#     extruded=True,
#     coverage=1)

# # Set the viewport location
# view_state = pdk.ViewState(
#     longitude=-1.415,
#     latitude=52.2323,
#     zoom=6,
#     min_zoom=5,
#     max_zoom=15,
#     pitch=40.5,
#     bearing=-27.36)

# # Combined all of it and render a viewport
# r = pdk.Deck(layers=[layer], initial_view_state=view_state)
# st.pydeck_chart(r)



