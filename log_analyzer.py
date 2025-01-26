import argparse
import csv
import re
from datetime import datetime
from pymongo import MongoClient
from fastapi import FastAPI
import uvicorn

def parse_log(file, level=None, st_time=None, end_time=None):
    logs = []
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) UserID:(\d+) (.+)")
    
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            match = pattern.match(line)
            if not match:
                print(f"Skipping malformed line: {line}")
                continue

            timestamp_str, log_level, user_id, message = match.groups()
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print(f"Skipping invalid timestamp: {timestamp_str}")
                continue

            if level and log_level.upper() != level.upper():
                continue
            if st_time and timestamp < st_time:
                continue
            if end_time and timestamp > end_time:
                continue

            logs.append({
                "timestamp": timestamp,
                "log_level": log_level,
                "user_id": user_id,
                "message": message
            })

    if not logs:
        print("No logs available after applying filters.")
    return logs

def write_to_csv(logs, output_file):
    if not logs:
        print("No logs to write to CSV.")
        return
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "log_level", "user_id", "message"])
        writer.writeheader()
        for log in logs:
            writer.writerow({
                "timestamp": log["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "log_level": log["log_level"],
                "user_id": log["user_id"],
                "message": log["message"]
            })
    print(f"CSV report saved to {output_file}")

def summarize_logs(logs):
    if not logs:
        print("No logs available for summary.")
        return
    
    start_time = min(log["timestamp"] for log in logs)
    end_time = max(log["timestamp"] for log in logs)
    log_levels = {"INFO": 0, "ERROR": 0, "WARN": 0}

    user_activity = {}

    for log in logs:
        log_levels[log["log_level"]] += 1
        user_activity[log["user_id"]] = user_activity.get(log["user_id"], 0) + 1

    most_active_user = max(user_activity, key=user_activity.get)

    print(f"Time duration: {start_time} - {end_time}")
    print(f"Number of logs by category: INFO={log_levels['INFO']} | WARN={log_levels['WARN']} | ERROR={log_levels['ERROR']}")
    print(f"Most active user: UserID {most_active_user}")

def insert_into_mongodb(logs, db_url):
    if not logs:
        print("No logs to insert into MongoDB.")
        return
    try:
        client = MongoClient(db_url)
        db = client["log_database"]
        collection = db["logs"]
        collection.insert_many(logs)
        print("Logs successfully inserted into MongoDB.")
    except Exception as e:
        print(f"Failed to insert into MongoDB: {e}")

app = FastAPI()

@app.get("/logs")
def get_logs(log_level: str = None, start_time: str = None, end_time: str = None):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["log_database"]
    collection = db["logs"]

    query = {}
    if log_level:
        query["log_level"] = log_level.upper()
    if start_time:
        query["timestamp"] = {"$gte": datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}
    if end_time:
        query["timestamp"]["$lte"] = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    logs = list(collection.find(query, {"_id": 0}))

    return {"logs": logs}

def main():
    parser = argparse.ArgumentParser(description="Analyze server log files.")
    parser.add_argument("--logfile", required=True, help="Path to the input log file")
    parser.add_argument("--output", help="Path to save the generated CSV report")
    parser.add_argument("--level", help="Filter logs by severity level (INFO, ERROR, WARN)")
    parser.add_argument("--st_time", help="Start timestamp to filter logs (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end_time", help="End timestamp to filter logs (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--summarize", action="store_true", help="Summarize the logs and display output")
    parser.add_argument("--db", help="MongoDB connection string to store logs")

    args = parser.parse_args()

    st_time = datetime.strptime(args.st_time, "%Y-%m-%d %H:%M:%S") if args.st_time else None
    end_time = datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S") if args.end_time else None

    logs = parse_log(args.logfile, args.level, st_time, end_time)

    if logs and args.output:
        write_to_csv(logs, args.output)

    if args.summarize:
        summarize_logs(logs)

    if args.db:
        insert_into_mongodb(logs, args.db)

if __name__ == "__main__":
    main()
