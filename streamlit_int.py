import streamlit as st
import requests

st.title("Log Analyzer UI")

log_level = st.selectbox("Log Level", options=["INFO", "ERROR", "WARN", "DEBUG", ""])
start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM:SS)")
end_time = st.text_input("End Time (YYYY-MM-DD HH:MM:SS)")

if st.button("Fetch Logs"):
    params = {}
    if log_level:
        params["log_level"] = log_level
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time
    response = requests.get("http://localhost:8000/logs", params=params)
    logs = response.json().get("logs", [])
    st.write(logs)
