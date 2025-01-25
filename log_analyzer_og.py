import argparse
import csv
from datetime import datetime
from pymongo import MongoClient

def parse_log(file, level=None, st_time=None, end_time=None):
    logs = []
    with open(file, 'r') as f:
        for line in f:
            parts = line.strip().split(" ", 4)
            if len(parts) < 5:
                continue
            timestamp, log_level, user_info, _, message = parts
            user_id = user_info.split(":")[1]
            log = {
                "timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                "log_level": log_level,
                "user_id": user_id,
                "message": message
            }
            if level and log_level != level:
                continue
            if st_time and log["timestamp"] < st_time:
                continue
            if end_time and log["timestamp"] > end_time:
                continue
            logs.append(log)
    return logs

def write_csv(logs, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "log_level", "user_id", "message"])
        writer.writeheader()
        for log in logs:
            writer.writerow({k: str(v) if k == "timestamp" else v for k, v in log.items()})

def summarize_logs(logs):
    start_time = min(log["timestamp"] for log in logs) if logs else None
    end_time = max(log["timestamp"] for log in logs) if logs else None
    log_levels = {log["log_level"] for log in logs}
    counts = {level: sum(1 for log in logs if log["log_level"] == level) for level in log_levels}
    users = {log["user_id"] for log in logs}
    most_active_user = max(users, key=lambda user: sum(1 for log in logs if log["user_id"] == user), default=None)
    print(f"Time Duration: {start_time} - {end_time}")
    print("Logs by Level:", counts)
    print("Most Active User:", most_active_user)

def insert_into_mongo(logs, conn_str):
    client = MongoClient(conn_str)
    db = client.log_analyzer
    collection = db.logs
    collection.insert_many(logs)

def main():
    parser = argparse.ArgumentParser(description="Log Analyzer Tool")
    parser.add_argument("--logfile", required=True, help="Path to the input log file")
    parser.add_argument("--output", required=False, help="Path to save the CSV report")
    parser.add_argument("--level", required=False, help="Filter logs by severity level (INFO, ERROR, WARN)")
    parser.add_argument("--st_time", required=False, help="Start timestamp to filter logs (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end_time", required=False, help="End timestamp to filter logs (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--summarize", action="store_true", help="Summarize logs and display output")
    parser.add_argument("--db", required=False, help="MongoDB connection string")

    args = parser.parse_args()
    st_time = datetime.strptime(args.st_time, "%Y-%m-%d %H:%M:%S") if args.st_time else None
    end_time = datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S") if args.end_time else None

    logs = parse_log(args.logfile, args.level, st_time, end_time)

    if args.output:
        write_csv(logs, args.output)
    if args.summarize:
        summarize_logs(logs)
    if args.db:
        insert_into_mongo(logs, args.db)

if __name__ == "__main__":
    main()
