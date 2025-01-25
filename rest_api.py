from fastapi import FastAPI, Query
from pymongo import MongoClient
from typing import List, Optional

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client.log_analyzer
collection = db.logs

@app.get("/logs")
def get_logs(log_level: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None):
    query = {}
    if log_level:
        query["log_level"] = log_level
    if start_time:
        query["timestamp"] = {"$gte": start_time}
    if end_time:
        query["timestamp"] = query.get("timestamp", {})
        query["timestamp"]["$lte"] = end_time
    logs = list(collection.find(query, {"_id": 0}))
    return {"logs": logs}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Log Analyzer API!"}
