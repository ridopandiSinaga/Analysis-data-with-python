import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
plt.style.use('dark_background')
from func import (
  create_monthly_users_df, create_seasonly_users_df, create_weatherly_users_df, create_hourly_users_df
)
 
# load dataset

df_day = pd.read_csv("dashboard/cleaned_bikeshare_day.csv")
df_hour = pd.read_csv("dashboard/cleaned_bikeshare_hour.csv")
df_day['date'] = pd.to_datetime(df_day['date'])
df_hour['date'] = pd.to_datetime(df_hour['date'])
st.set_page_config(
    page_title="Capital Bikeshare: Bike-sharing Dashboard",
    page_icon="bar_chart:",
    layout="wide"
    )


# make filter components (komponen filter)

min_date = df_day["date"].min()
max_date = df_day["date"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # add capital bikeshare logo
    st.markdown("[![image](https://github.com/ridopandiSinaga/Test/assets/89272004/9f338243-a682-400c-97c1-ea5b2c069fa2)]()")

    st.sidebar.header("Filter:")
    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Visit my Profile:")

st.sidebar.markdown("Ridopandi Sinaga")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/ridopandi-sinaga/)")
with col2:
    st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/ridopandiSinaga)")

# hubungkan filter dengan main_df

main_df_day = df_day[
    (df_day["date"] >= str(start_date)) &
    (df_day["date"] <= str(end_date))
]
main_df_hour = df_hour[
    (df_hour["date"] >= str(start_date)) &
    (df_hour["date"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_df_day)
seasonly_users_df = create_seasonly_users_df(main_df_day)
hourly_users_df = create_hourly_users_df(main_df_hour)
weatherly_users_df = create_weatherly_users_df(main_df_day)

# ----- MAINPAGE -----
st.title("Bike-Sharing Dashboard")
st.markdown("![image](https://github.com/ridopandiSinaga/Test/assets/89272004/93c11ad6-c1b2-4ac9-b4e5-3d66d741ca4e)")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df_day['count'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df_day['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df_day['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# ----- CHART -----
fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["skyblue", "orange", "green"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)


fig_week = px.bar(df_day, 
                  x=df_day.index, 
                  y=['casual', 'registered'],
                 color_discrete_sequence=["blue", "green"],
                 labels={'value': 'Count', 'weekday': 'Day'},
                 title='Casual vs Registered Count by Weekday',
                 template='plotly_white',
                 barmode='group')

# Line plot untuk 'cnt'
fig_week.add_scatter(x=df_day.index, y=df_day['count'], mode='lines+markers', name='count', line=dict(color='red'))
st.plotly_chart(fig_week, use_container_width=True)
# --------
fig = px.line(hourly_users_df,
              x='hour',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=["skyblue", "orange"],
              markers=True,
              title='Count of bikeshare rides by hour of day').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)
# ----------------
fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["skyblue", "orange", "green"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')


fig2 = px.bar(weatherly_users_df,
              x='weather',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange" , "green"],
              title='Count of bikeshare rides by weather').update_layout(xaxis_title='', yaxis_title='Total Rides')


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

# ------------------------

fig3 = px.scatter(df_day, x='temp', y='count', color='season', title='Clusters of bikeshare rides count by season and temperature')
fig4 = px.scatter(df_day, x='humidity', y='count', color='season', title='Clusters of bikeshare rides count by season and humidity')
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_container_width=True)

# ------------------------------
fig5 = px.pie(df_day, values='count', names='season',
                    title='Percentage of Bike-share Users by Season',
                    color_discrete_sequence=['gold', 'tomato', 'cornflowerblue', 'orchid'],
                    labels={'count': 'Percentage'})
fig5.update_layout(legend=dict(orientation="v", yanchor="bottom", y=0.8, xanchor="right", x=0.2))
fig6 = px.bar(df_day, 
                  x=df_day['season'], 
                  y=['casual', 'registered'],
                  color_discrete_sequence=["blue", "green"],
                  labels={'value': 'Count', 'season': 'Season'},
                  title='Casual vs Registered Count by Season',
                  template='plotly_white',
                  barmode='group')


left_column, right_column = st.columns((1.5,2))
left_column.plotly_chart(fig5, use_container_width=True)
right_column.plotly_chart(fig6, use_container_width=True)

expander1 = st.expander(label="Insight")
with expander1:
            """
            Analyzing the visualizations provided earlier yields the following findings:

            - Approximately 70% of bike-sharing users are registered, with the remaining 30% being casual users.
            - Over a 2-year span, monthly trends indicate spikes in bike-share rides during January, March, May, July, August, and September. Conversely, decreases are observed in February, April, June, October, and November.
            - Examining daily patterns reveals that Fridays experience the highest overall rental activity, encompassing both registered and casual users. However, when considering each group separately, registered users tend to rent more on weekdays, while casual users favor weekends.
            - Hourly trends indicate a surge in bike-share rides from 5 am to 10 am, followed by a decline in the afternoon and evening.
            - The distribution of customers across seasons is most pronounced in the Fall, constituting approximately 80% of total rentals from early September to late November. This seasonal pattern holds true for both registered and casual users.
            - Rental numbers are significantly influenced by weather conditions, with clear weather attracting more bike-share rides and worsening conditions leading to a decrease in rentals.
            """

st.caption('Copyright (c), Created by Ridopandi Sinaga')

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)