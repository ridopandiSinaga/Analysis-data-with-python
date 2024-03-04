import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
plt.style.use('dark_background')


# create helper functions

def create_monthly_users_df(df_day):
    monthly_users_df = df_day.resample(rule='M', on='date').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df_day):
    seasonly_users_df = df_day.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weatherly_users_df(df_day):
    weatherly_users_df = df_day.groupby("weather").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    weatherly_users_df = weatherly_users_df.reset_index()
    weatherly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weatherly_users_df = pd.melt(weatherly_users_df,
                                      id_vars=['weather'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weatherly_users_df['weather'] = pd.Categorical(weatherly_users_df['weather'],
                                             categories=['Clear/Partly Cloudy','Misty/Cloudy','Light Snow/Rain','Severe Weather'])
    weatherly_users_df = weatherly_users_df.sort_values('weather')
    
    return weatherly_users_df

def create_hourly_users_df(df_hour):
    hourly_users_df = df_hour.groupby('hour').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df
