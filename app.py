import streamlit as st

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="TaxiFare | NYC",
    page_icon="🚕",
    layout="wide"
)

api_url = st.secrets["API_URL"]

# Custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #F5F5F5;
        color: #171717;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
    }

    .hero {
        background-color: #171717;
        padding: 35px;
        border-radius: 20px;
        margin-bottom: 30px;
    }

    .hero h1 {
        color: #FFD600;
        font-size: 48px;
        margin: 0;
    }

    .hero p {
        color: #DDDDDD;
        font-size: 17px;
        margin-bottom: 0;
    }

    div.stButton > button {
        background-color: #FFD600;
        color: #171717;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        height: 50px;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #E5C100;
        color: #171717;
    }

    .fare-card {
        background-color: #171717;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }

    .fare-card h2 {
        color: #FFD600;
        font-size: 60px;
        margin: 0;
    }

    .fare-card p {
        color: #DDDDDD;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero">
    <h1>🚕 TaxiFare NYC</h1>
    <p>Your journey. Your destination. Know your fare before you go.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Plan your journey")

    st.markdown("#### 📍 Pickup location")

    col1, col2 = st.columns(2)

    with col1:
        pickup_latitude = st.number_input(
            "Pickup latitude",
            value=40.7580,
            min_value=-90.0,
            max_value=90.0,
            format="%.6f"
        )

    with col2:
        pickup_longitude = st.number_input(
            "Pickup longitude",
            value=-73.9855,
            min_value=-180.0,
            max_value=180.0,
            format="%.6f"
        )

    st.markdown("#### 🏁 Drop-off location")

    col3, col4 = st.columns(2)

    with col3:
        dropoff_latitude = st.number_input(
            "Drop-off latitude",
            value=40.7829,
            min_value=-90.0,
            max_value=90.0,
            format="%.6f"
        )

    with col4:
        dropoff_longitude = st.number_input(
            "Drop-off longitude",
            value=-73.9654,
            min_value=-180.0,
            max_value=180.0,
            format="%.6f"
        )

    st.markdown("#### 🕒 Journey details")

    col5, col6 = st.columns(2)

    with col5:
        pickup_date = st.date_input(
            "Pickup date",
            value=datetime.now().date()
        )

    with col6:
        pickup_time = st.time_input(
            "Pickup time",
            value=datetime.now().time()
        )

    passenger_count = st.slider(
        "Number of passengers",
        min_value=1,
        max_value=6,
        value=1
    )

    predict = st.button("Estimate my fare")

with right:
    st.subheader("Your journey map")

    map_data = pd.DataFrame({
        "lat": [pickup_latitude, dropoff_latitude],
        "lon": [pickup_longitude, dropoff_longitude],
        "color": ["#16A34A", "#DC2626"]
    })

    st.map(
        map_data,
        color="color",
        size=100,
        zoom=12
    )

    st.caption("🟢 Pickup location  |  🔴 Drop-off location")

    if predict:
        pickup_datetime = datetime.combine(
            pickup_date,
            pickup_time
        ).strftime("%Y-%m-%d %H:%M:%S")

        params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
        }

        try:
            with st.spinner("Calculating your estimated fare..."):
                response = requests.get(
                    api_url,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()
                fare = float(response.json()["fare"])

            st.markdown(f"""
            <div class="fare-card">
                <p>ESTIMATED TAXI FARE</p>
                <h2>${fare:.2f}</h2>
                <p>Powered by Machine Learning</p>
            </div>
            """, unsafe_allow_html=True)

            st.caption(
                "This is an estimated fare, not a guaranteed price."
            )

        except (requests.RequestException, ValueError, KeyError):
            st.error(
                "Unable to calculate your fare. "
                "Please try again."
            )

    else:
        st.info("Enter your journey details to estimate your fare.")

st.divider()

st.caption(
    "TaxiFare NYC • Machine Learning • FastAPI • Google Cloud • Streamlit"
)
