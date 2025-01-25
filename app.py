# import streamlit as st
# import requests

# # FastAPI URL (replace with your FastAPI deployed URL)
# FASTAPI_URL = "https://herokuyt.onrender.com"

# def fetch_logs(log_level, start_time, end_time):
#     params = {}
#     if log_level:
#         params["log_level"] = log_level
#     if start_time:
#         params["start_time"] = start_time
#     if end_time:
#         params["end_time"] = end_time
    
#     response = requests.get(FASTAPI_URL, params=params)
#     if response.status_code == 200:
#         return response.json()["logs"]
#     else:
#         st.error(f"Failed to fetch logs. Status code: {response.status_code}")
#         return []

# # Streamlit App UI
# st.title("Log Analyzer Dashboard")

# log_level = st.selectbox("Log Level", ["INFO", "ERROR", "WARN", "ALL"])
# start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM:SS)")
# end_time = st.text_input("End Time (YYYY-MM-DD HH:MM:SS)")

# if st.button("Get Logs"):
#     logs = fetch_logs(log_level, start_time, end_time)
    
#     if logs:
#         st.write(f"Found {len(logs)} logs")
#         for log in logs:
#             st.write(f"Timestamp: {log['timestamp']}, Level: {log['log_level']}, UserID: {log['user_id']}, Message: {log['message']}")
#     else:
#         st.write("No logs found.")
