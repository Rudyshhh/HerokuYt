import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/logs"

st.title("Log Analyzer")

log_level = st.selectbox("Select Log Level", ["INFO", "ERROR", "WARN"])
start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM:SS)")
end_time = st.text_input("End Time (YYYY-MM-DD HH:MM:SS)")

if st.button("Get Logs"):
    params = {"log_level": log_level, "start_time": start_time, "end_time": end_time}
    response = requests.get(API_URL, params=params)
    data = response.json().get("logs", [])
    df = pd.DataFrame(data)
    st.write(df)
