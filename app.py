import streamlit as st
from agent import Agent
import folium
import pandas as pd
from streamlit_folium import folium_static
from center_info import CenterInfo
from currency_info import CurrencyInfo
from map_info import Itinerary
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("API_KEY")

# Initialize the agent with the API key
agent = Agent(api_key)

# Set page configuration
st.set_page_config(layout='wide')
st.title('TravellAIng')

# Initialize session state
def initialize_session_state():
    if "center" not in st.session_state:
        st.session_state.center = [48.9, 2.4]
    if "zoom" not in st.session_state:
        st.session_state.zoom = 10
    if "marker" not in st.session_state:
        st.session_state.marker = []

# Initialize map
def initialize_map(center, zoom):
    if "map" not in st.session_state or st.session_state.map is None:
        st.session_state.center = center
        st.session_state.zoom = zoom
        folium_map = folium.Map(location=st.session_state.center, zoom_start=st.session_state.zoom)
        st.session_state.map = folium_map
    return st.session_state.map

# Reset session state
def reset_session_state():
    for key in list(st.session_state.keys()):
        if key not in ["center", "zoom"]:
            del st.session_state[key]
    initialize_session_state()

# Display app description
st.write("""
    This app predicts the **Tourism**!
""")

initialize_session_state()

# Layout columns
col1, col2 = st.columns(2)

with col1:
    request = st.text_area("Onde você gostaria de ir?")
    button = st.button("Pedir sugestão de roteiro")
    box = st.container()
    with box:
        container = st.empty()
        container.header("Itinerário")

# Handle button click and request
if button and request:
    reset_session_state()
    itinerary = agent.get_itinerary(request)
    try:
        container.write(itinerary['agent_suggestion'])
    except KeyError:
        container.write("Desculpe, não consegui encontrar um roteiro para você.")
    
    try:
        points_coordinates = []
        itinerary_map_result = Itinerary.from_json(itinerary['coordinates'])
        for day in itinerary_map_result.days:
            for loc in day.locations:
                points_coordinates.append((loc.lat, loc.lon))
        st.session_state["marker"] = [folium.Marker(location=point) for point in points_coordinates]
    except KeyError:
        pass

    center_info = CenterInfo.from_json(itinerary['center_info'])
    st.session_state.center = center_info.center
    st.session_state.zoom = center_info.zoom 

with col2:
    folium_map = initialize_map(st.session_state.center, st.session_state.zoom)
    fg = folium.FeatureGroup(name="Markers")
    for marker in st.session_state["marker"]:
        fg.add_child(marker)
    fg.add_to(folium_map)
    folium_static(folium_map)

col3 = st.container()
with col3:
    if button and request:
        try:
            if itinerary.get('currency_info'):
                currency_info = CurrencyInfo.from_json(itinerary['currency_info'])

                st.subheader("Informação de Moeda")
                st.write(f"Código: {currency_info.currency_code}")
                st.write(f"Nome: {currency_info.name}")
                st.write(f"Símbolo: {currency_info.symbol}")
                st.subheader("Valores de Câmbio:")
                for val in currency_info.value:
                    st.write(f"{val.name} ({val.currency_code}): {val.symbol}{val.current_value}")
            else:
                st.write("Sem informações de moeda.")
        except KeyError:
            st.write("Sem informações de moeda.")
