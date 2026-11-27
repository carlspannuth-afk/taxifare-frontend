import streamlit as st
import requests


api_url = st.secrets["API_URL"]


pickup_datetime = st.text_input('pickup_datetime:')
pickup_longitude = st.number_input('pickup_longitude')
pickup_latitude = st.number_input('pickup_latitude')
dropoff_longitude = st.number_input('dropoff_longitude')
dropoff_latitude = st.number_input('dropoff_latitude')
passenger_count = st.number_input('passenger_count', min_value=1, step=1, value=1)

if st.button('predict'):

    params = {'pickup_datetime': pickup_datetime,
            'pickup_longitude': pickup_longitude,
            'pickup_latitude': pickup_latitude,
            'dropoff_longitude': dropoff_longitude,
            'dropoff_latitude': dropoff_latitude,
            'passenger_count': passenger_count
            }


    response = requests.get(api_url, params=params)
    st.write('Fare:', response.json()['fare'])
