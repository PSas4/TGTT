import streamlit as st
import requests

# Set Page Configuration
st.set_page_config(page_title="Taxi Billing Software", page_icon="🚖", layout="centered")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #222222; color: white; }
    .title { font-size: 36px; font-weight: bold; color: #ffcc00; text-align: center; }
    .subtitle { font-size: 20px; font-weight: bold; color: #cccccc; text-align: center; margin-bottom: 20px; }
    .stTextInput label, .stNumberInput label { color: #ffcc00 !important; font-size: 16px; font-weight: bold; }
    .stButton button { background-color: #ff6600 !important; color: white !important; border-radius: 8px !important; font-size: 18px !important; padding: 10px 20px !important; }
    .stAlert { background-color: #333333 !important; border-left: 5px solid #ffcc00 !important; color: white !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with Emoji
st.markdown('<p class="title">🚖 Taxi Billing Software</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Calculate your fare and generate a bill instantly!</p>', unsafe_allow_html=True)

# Layout with Columns for Better Design
col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("🧑 Customer Name", placeholder="Enter customer name")
    start_reading = st.number_input("🏁 Start Meter Reading", min_value=0.0, format="%.2f")
    toll = st.number_input("🚧 Toll Charges (₹)", min_value=0.0, format="%.2f")

with col2:
    rate_per_km = st.number_input("💰 Rate per km (₹)", min_value=0.0, format="%.2f")
    end_reading = st.number_input("🏁 End Meter Reading", min_value=0.0, format="%.2f")
    state_tax = st.number_input("🏛️ State Charges (₹) (If Applicable)", min_value=0.0, format="%.2f")

meal = st.number_input("🍽️ Meal Charges (₹) (If Applicable)", min_value=0.0, format="%.2f")
night_stay = st.number_input("🏨 Night Stay Charges (₹) (If Applicable)", min_value=0.0, format="%.2f")

st.markdown("---")  # Horizontal Line for Separation

# Calculate Fare Button
if st.button("📊 Calculate Fare"):
    with st.spinner("Calculating fare... ⏳"):
        try:
            response = requests.post("http://127.0.0.1:5000/calculate", json={
                "start_reading": start_reading,
                "end_reading": end_reading,
                "rate_per_km": rate_per_km,
                "toll": toll,
                "state_tax": state_tax,
                "meal": meal,
                "night_stay": night_stay
            }, timeout=10)

            result = response.json()
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"✅ Total Fare: ₹{result['total_fare']:.2f} | Distance: {result['distance']} km")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Connection error: {e}")

st.markdown("---")  # Horizontal Line for Separation

# Generate Bill Button
if st.button("📜 Generate Bill"):
    with st.spinner("Saving the bill... 💾"):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/save", 
                json={
                    "customer_name": customer_name,
                    "start_reading": start_reading,
                    "end_reading": end_reading,
                    "rate_per_km": rate_per_km,
                    "toll": toll,
                    "state_tax": state_tax,
                    "meal": meal,
                    "night_stay": night_stay
                }, 
                timeout=30  # Increased timeout
            )

            result = response.json()
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                st.success("🎉 Bill saved successfully!")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Connection error: {e}")
