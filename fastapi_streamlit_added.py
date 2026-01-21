import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("📅 Booking System")

# 1. Create Slot
st.subheader("Create Slot")
time_input = st.text_input("Enter Slot Time (e.g., 10:00 AM)")
if st.button("Create Slot"):
    if time_input:
        resp = requests.post(f"{BASE_URL}/slot/create", params={"time": time_input})
        st.success(resp.json())
    else:
        st.error("Please enter a valid time")

# 2. Book Slot
st.subheader("Book Slot")
col1, col2 = st.columns(2)
slot_id = col1.number_input("Slot ID to Book", min_value=1, step=1)
user_name = col2.text_input("Your Name")
if st.button("Book Slot"):
    if user_name:
        resp = requests.post(f"{BASE_URL}/slot/book/{slot_id}", params={"user": user_name})
        st.success(resp.json())
    else:
        st.error("Enter your name")

# 3. Cancel Slot
st.subheader("Cancel Booking")
cancel_id = st.number_input("Slot ID to Cancel", min_value=1, step=1)
if st.button("Cancel Booking"):
    resp = requests.delete(f"{BASE_URL}/slot/cancel/{cancel_id}")
    st.success(resp.json())

# 4. Show All Slots
if st.button("Show All Slots"):
    resp = requests.get(f"{BASE_URL}/slots")
    st.table(resp.json())

# 5. Show Available Slots
if st.button("Show Available Slots"):
    resp = requests.get(f"{BASE_URL}/slots/available")
    st.table(resp.json())
