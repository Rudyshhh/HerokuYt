from fastapi import FastAPI, Query
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["log_database"]
collection = db["logs"]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Log Analyzer API!"}

@app.get("/logs")
def get_logs(log_level: str = None, start_time: str = None, end_time: str = None):
    query = {}
    if log_level:
        query["log_level"] = log_level.upper()
    if start_time:
        query["timestamp"] = {"$gte": datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}
    if end_time:
        query["timestamp"]["$lte"] = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    logs = list(collection.find(query, {"_id": 0}))
    return {"logs": logs}
