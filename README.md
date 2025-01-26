# Log Analyzer Project

This project provides a log analysis system with a **FastAPI backend**, a **Streamlit frontend**, and a **CLI tool** for processing log files. It allows users to filter, summarize, and store log data in MongoDB.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Deployment on Render](#deployment-on-render)
4. [Usage](#usage)
5. [File Explanations](#file-explanations)
6. [API Endpoints](#api-endpoints)
7. [Troubleshooting](#troubleshooting)




## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rudyshhh/HerokuYt.git
   cd HerokuYt
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Deployment on Render

Follow these steps to deploy the FastAPI backend on Render.

### 1. Setup Render Account

- Go to [Render.com](https://render.com) and sign in.
- Create a new **"Web Service."**

### 2. Configure the Service

- **Repository:** Connect your GitHub repo containing this project.
- **Build Command:**  
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**  
  ```bash
  uvicorn api:app --host 0.0.0.0 --port 8000
  ```
- **Environment Variables:**  
  Add `MONGO_URI` with your MongoDB connection string.

### 3. Deploy the Service

- Click **"Deploy"**, and wait for the service to go live.
- Once deployed, Render provides a live URL:  
  ```
  https://herokuyt.onrender.com
  ```

### 4. Verify the Deployment

- Open a browser and visit the URL:  
  ```
  https://herokuyt.onrender.com/docs
  ```
- You should see the FastAPI interactive UI.

---

## Usage

### 1. Running the FastAPI Backend (Locally)

Start the FastAPI server with:

```bash
uvicorn api:app --reload
```
Once the server is running, you can access the API at: http://127.0.0.1:8000/docs.

You can now use both FastAPI and Streamlit:

FastAPI: Access the API endpoints directly from the browser or use a tool like curl or Postman to send requests to the API.

Streamlit: Run the Streamlit UI in a separate terminal with the following command:

``` bash

streamlit run ui.py
```
This will launch the frontend, allowing you to interact with the FastAPI backend via the graphical interface.

### 2. Running the CLI Tool

The CLI tool processes log files and stores data in MongoDB.

Example commands:

- Parse and store logs in MongoDB:
  ```bash
  python log_analyzer.py --logfile sample.log --db "mongodb+srv://r11mehta:junejune@cluster0.0ip1h.mongodb.net"
  ```

- Filter logs by level:
  ```bash
  python log_analyzer.py --logfile sample.log --level ERROR --output filtered_logs.csv
  ```

- Summarize logs:
  ```bash
  python log_analyzer.py --logfile sample.log --summarize
  ```

---

### 3. Running the Streamlit UI

Before running the Streamlit frontend, you need to deploy the FastAPI backend on Render.

#### 1. Deploy the FastAPI Backend on Render

Follow the steps in the **Deployment on Render** section of this README to deploy the FastAPI backend. Once the backend is deployed, Render will provide a live URL.

#### 2. Run the Streamlit Frontend

To start the Streamlit frontend:

```bash
streamlit run ui.py
```

## File Explanations

### 1. `api.py` (FastAPI Backend)

Handles API requests to fetch logs from MongoDB.

- **Endpoints:**
  - `GET /` → Welcome message.
  - `GET /logs` → Retrieve logs with optional filters.

---

### 2. `log_analyzer.py` (CLI Tool)

Processes log files, filters data, generates CSV reports, and uploads logs to MongoDB.

Functions included:

- `parse_log(file, level, st_time, end_time)`: Parses logs.
- `write_to_csv(logs, output_file)`: Saves logs to CSV.
- `summarize_logs(logs)`: Provides summary reports.
- `insert_into_mongodb(logs, db_url)`: Uploads logs to MongoDB.

---

### 3. `ui.py` (Streamlit Frontend)

A web-based interface to interact with the FastAPI backend.

- Allows users to query logs by log level and time range.
- Displays results in a table.

---

## API Endpoints

### 1. `GET /`

**Description:**  
Returns a welcome message.

**Example Response:**

```json
{
  "message": "Welcome to the Log Analyzer API!"
}
```

---

### 2. `GET /logs`

**Description:**  
Fetch logs with optional query parameters.

**Query Parameters:**

- `log_level`: (Optional) Filter by log level (INFO, ERROR, WARN).
- `start_time`: (Optional) Start time (YYYY-MM-DD HH:MM:SS).
- `end_time`: (Optional) End time (YYYY-MM-DD HH:MM:SS).

**Example Request:**

```
https://herokuyt.onrender.com/logs?log_level=ERROR&start_time=2024-01-01 00:00:00
```

**Example Response:**

```json
{
  "logs": [
    {
      "timestamp": "2024-01-20 14:33:22",
      "log_level": "ERROR",
      "user_id": "12345",
      "message": "Failed to connect to database"
    }
  ]
}
```

---

## Troubleshooting

### 1. Common Deployment Issues

- **502 Bad Gateway:**  
  - Check if your `start command` is correct.
  - Ensure MongoDB URI is correctly set in Render environment variables.

- **404 Not Found:**  
  - Check if you are using the correct endpoint (e.g., `/logs` instead of root `/`).

- **Connection Timeout:**  
  - Ensure MongoDB Atlas allows access from all IPs or your server's IP.

---

