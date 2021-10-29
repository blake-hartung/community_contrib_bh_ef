import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import datetime as dt
import pydeck as pdk
import numpy as np



st.title("Streamlit Tutorial")

uber_files = ['uber-raw-data-apr14.csv']

ubers_df = pd.DataFrame()
for file in uber_files:
    df = pd.read_csv(file,encoding='utf-8')
    ubers_df = pd.concat([df,ubers_df])

# Allow user to select frac of data to analyze
st.caption("Streamlit allows for the user to customize their EDAV experience")
st.write("### Geo-Data from Uber")
user_frac=st.slider("CHoose fraction of data", min_value=0.01, max_value=1.0)
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

"""Start Iris Tutorial"""

# this is the simplest streamlit function for adding text to a page
# notice streamlit unerstands markdown formatting!
st.write('### The Infamous **Iris** Dataset')

# file_uploader returns the values within the file given by a user!
csv_data = st.file_uploader('Upload the Iris Data Here!')

# simple local image calling for input into app (looks nice!)
st.image("iris.jpeg")

# streamlit expander, useful if mor info is wanted about something but
# you dont want to clutter the page up
with st.expander("Click for more information on the iris dataset"):
    st.write("The Iris flower data set or Fisher's Iris data set is a multivariate data set introduced by the British statistician and biologist Ronald Fisher in his 1936 paper The use of multiple measurements in taxonomic problems as an example of linear discriminant analysis. It is sometimes called Anderson's Iris data set because Edgar Anderson collected the data to quantify the morphologic variation of Iris flowers of three related species. Two of the three species were collected in the Gaspé Peninsula all from the same pasture, and picked on the same day and measured at the same time by the same person with the same apparatus")
    st.write("The data set consists of 50 samples from each of three species of Iris (Iris setosa, Iris virginica and Iris versicolor). Four features were measured from each sample: the length and the width of the sepals and petals, in centimeters. Based on the combination of these four features, Fisher developed a linear discriminant model to distinguish the species from each other.")
    st.write("Source: Wikipedia")

try:
    df = pd.read_csv(csv_data)


    st.write("**Let's look at a few lines:**")
    st.write("Notice how these change every time a selection is made elsewhere.")

    # st dataframe is used for displaying dataframe objects
    st.dataframe(df.sample(6))

    # the multiselect tool allows user input of one or more given variables
    # here we see the 3 species (returns a list of strings)
    choices = st.multiselect("Now Narrow it down a little bit", ["Virginica", "Setosa", "Versicolor"])

    df_filt = df[df['variety'].isin(choices)]

    st.dataframe(df_filt)

    st.write("**How about we try to plot what we have:**")

    # creation of a scatter plot based on filter choices
    fig, ax = plt.subplots()
    for spec in np.unique(df_filt['variety']):
        df_now = df_filt[df_filt['variety'] == spec]
        ax.scatter(df_now['sepal.length'], df_now['sepal.width'],
                   s=20, label=spec, alpha=0.8)
    ax.legend()
    ax.set_ylabel("Sepal Width")
    ax.set_xlabel("Sepal Length")

    # This function is used for showing a matplotlib figure on your app
    st.pyplot(fig)

    st.write('**How do these compare to one another?**')

    # radio button addition to the page (returns a string)
    choice = st.radio("Choose one:", ["Virginica", "Setosa", "Versicolor"])

    df_spec = df[df["variety"] == choice]

    st.write("Summary statistics for ", choice)

    # below is the streamlit metrics row. You have to specify all aspects of information
    # that will be given on the metric specifically, it doesnt come up with it for you
    cols = st.columns(4)
    cols[0].metric("Sepal Length", value=np.around(df_spec["sepal.length"].mean(), 2),
                  delta=np.around(df_spec["sepal.length"].mean() - df["sepal.length"].mean(), 2))
    cols[1].metric("Sepal Width", value=np.around(df_spec["sepal.width"].mean(), 2),
                  delta=np.around(df_spec["sepal.width"].mean() - df["sepal.width"].mean(), 2))
    cols[2].metric("Petal Length", value=np.around(df_spec["petal.length"].mean(), 2),
                  delta=np.around(df_spec["petal.length"].mean() - df["petal.length"].mean(), 2))
    cols[3].metric("Petal Width", value=np.around(df_spec["petal.width"].mean(), 2),
                  delta=np.around(df_spec["petal.width"].mean() - df["petal.width"].mean(), 2))


except ValueError:
    st.write("No data has been uploaded")

st.write('**More info on other Streamlit Input Widgets!**')
with st.expander("Expand This"):

    click = st.button("Click Me")
    st.write(type(click))

    st.download_button('Iris Photo Download', 'iris.jpeg')

    select = st.checkbox('Checkbox here!')
    st.write(type(select))

    number = st.slider('Pick your favorite number')
    st.write(type(number))

    input_text = st.text_input('Write anything you want here')
    st.write(type(input_text))

    number_input = st.number_input("Guess a number between 1 - 10:", 0, 10)
    if number_input == 7:
        st.write('Correct!')
    else:
        st.write("Wrong Guess!")
    st.write(type(number_input))

    time_input = st.time_input('What time is it?')
    st.write(type(time_input))

    color = st.color_picker('Where is your favorite color?')
    st.write(color)
    st.write(type(color))

st.write('**More info on plotting features in Streamlit!**')
with st.expander('Expand This'):
    df2 = pd.DataFrame((np.random.rand(50) * 3) - 1.5)
    df3 = pd.DataFrame({'idx': ['A', 'B', 'C'],
                        'stat1': np.random.rand(3),
                        'stat2': np.random.rand(3)}).set_index('idx')
    st.write("Built-in Streamlit Charts (Usable with pd.DataFrame)")

    st.code("st.line_chart(df)")
    st.line_chart(df2)

    st.code("st.areas_chart(df)")
    st.area_chart(df2)

    st.code("st.bar_chart(df)")
    st.bar_chart(df3)

    st.write('Also compatible with:')

    st.write("- Altair")
    st.code("st.altair_chart(altair_figure)")

    st.write("- Vega-Lite")
    st.code("st.vega_lite_chart(vega_declaratives)")

    st.write("- Plotly")
    st.code("st.plotly_chart(plotly_figure)")

    st.write("- Bokeh")
    st.code("st.bokeh_chart(bokeh_figure)")

    st.write("- GraphViz")
    st.code("st.graphviz_chart(graphvis_spec)")