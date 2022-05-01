import streamlit as st
from datetime import datetime
import requests
from streamlit_folium import st_folium
import folium

LOCAL_URL = "http://localhost:8000/"
PROD_URL = "https://lewagon-hfw5yigd4a-ue.a.run.app/predict"

st.markdown('''
# NYC Taxi Fare Prediction
Input parameters here to find out how much your NYC taxi ride is estimated to cost!
''')

pickup_selected = "pu_coords" in st.session_state and st.session_state.get("pu_coords")
dropoff_selected = "do_coords" in st.session_state and st.session_state.get("do_coords")
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

if pickup_selected and dropoff_selected:
  pickup_latitude, pickup_longitude = st.session_state.pu_coords
  dropoff_latitude, dropoff_longitude  = st.session_state.do_coords
  m = folium.Map(location=[dropoff_latitude, dropoff_longitude], zoom_start=16)

  folium.Marker(
      [pickup_latitude, pickup_longitude], tooltip='Pickup'
  ).add_to(m)
  folium.Marker(
      [dropoff_latitude, dropoff_longitude], tooltip='Dropoff'
  ).add_to(m)

elif pickup_selected:
  st.markdown("### Please select dropoff location 🗺️")
  pickup_latitude, pickup_longitude = st.session_state.pu_coords
  m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=16)
  folium.Marker(
      [pickup_latitude, pickup_longitude], tooltip='Pickup'
  ).add_to(m)
else:
  st.markdown("### Please select pickup location 🗺️")

map_returns = st_folium(m)

if pickup_selected and map_returns.get("last_clicked"):
  print('DO CLICKED')
  print(map_returns)
  dropoff_coords = map_returns.get("last_clicked")
  dropoff_longitude, dropoff_latitude = dropoff_coords['lng'], dropoff_coords['lat']
  st.session_state.do_coords = [dropoff_latitude, dropoff_longitude]
elif map_returns.get("last_clicked"):
  print('PU CLICKED')
  print(map_returns)
  pickup_coords = map_returns.get("last_clicked")
  pickup_longitude, pickup_latitude = pickup_coords['lng'], pickup_coords['lat']
  st.session_state.pu_coords = [pickup_latitude, pickup_longitude]


# '''
# ## What's the pickup date?
# '''

# from datetime import date
# pickup_date = st.date_input(
#     "What's the pickup date?",
#     date(2019, 7, 6))
# st.write('Pickup datetime is:', pickup_date)

# '''
# ## What's the pickup time?
# '''
# from datetime import time
# pickup_time = st.time_input('Input pickup time', time(8, 45))

# st.write('Pickup time is', pickup_time)

'''
## What's the passenger count?
'''
passenger_count = st.slider("Passenger Count", 1, 8, 2)

st.write('The current number is ', passenger_count)

pickup_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if pickup_selected and dropoff_selected:
    params = {'key': '2013-07-06 17:18:00.000000119',
                "pickup_datetime": pickup_datetime,
                "pickup_longitude": pickup_longitude,
                "pickup_latitude": pickup_latitude,
                "dropoff_longitude": dropoff_longitude,
                "dropoff_latitude": dropoff_latitude,
                "passenger_count": passenger_count
    }
    response = requests.get(PROD_URL, params=params)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        prediction = response.json().get('fare')

        if st.button('Submit'):
            st.write(f'The predicted fare is ${round(prediction, 2)}')

    if st.button('Reset coords'):
        st.session_state.pu_coords = None
        st.session_state.do_coords = None
