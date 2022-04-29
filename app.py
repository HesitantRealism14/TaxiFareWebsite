import streamlit as st
import numpy as np
import pandas as pd
import datetime
from datetime import datetime
import requests
import pytz

st.markdown('''# TaxiFareModel
## NYC Taxi Fare Prediction
Input params here to find out how much your NYC taxi ride is estimated to cost!
''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

'''
## What's the pickup date?
'''

from datetime import date
pickup_date = st.date_input(
    "What's the pickup date?",
    date(2019, 7, 6))
st.write('Pickup datetime is:', pickup_date)

'''
## What's the pickup time?
'''
from datetime import time
pickup_time = st.time_input('Input pickup time', time(8, 45))

st.write('Pickup time is', pickup_time)


'''
## What's the pickup longitude?
'''
pickup_longitude = st.number_input('Insert a number', key='001')

st.write('The current number is ', pickup_longitude)

'''
## What's the pickup latitude?
'''
pickup_latitude = st.number_input('Insert a number', key='002')

st.write('The current number is ', pickup_latitude)

'''
## What's the dropoff longitude?
'''
dropoff_longitude = st.number_input('Insert a number', key='003')

st.write('The current number is ', dropoff_longitude)

'''
## What's the dropoff latitude?
'''
dropoff_latitude = st.number_input('Insert a number', key='004')

st.write('The current number is ', dropoff_latitude)


'''
## What's the passenger count?
'''
passenger_count = st.slider("Passenger Count", 1, 8, 2)

st.write('The current number is ', passenger_count)

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

url = 'https://lewagon-hfw5yigd4a-ue.a.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''

# df = pd.DataFrame({
#     'first column': list(range(1, 11)),
#     'second column': np.arange(10, 101, 10)
# })
# line_count = st.slider('Select a line count', 1, 10, 3)

# head_df = df.head(line_count)

pickup_datetime = datetime.combine(pickup_date, pickup_time)
# eastern = pytz.timezone("US/Eastern")
# pickup_datetime = eastern.localize(datetime.strptime(str(pickup_datetime), "%Y-%m-%d %H:%M:%S"), is_dst=None).astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
params = {'key': '2013-07-06 17:18:00.000000119',
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
}
response = requests.get(url, params=params).json()
prediction = response.get('fare')

st.write('#The predicted fare is ', prediction)
