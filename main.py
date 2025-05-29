from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import json

app = FastAPI()

# Serve static dashboard files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

# 🔍 Directory where all apps are deployed
PARENT_DIR = "/home/VaniSatya"

# 🔎 Find app folders with logs/
def discover_apps(base_dir):
    apps = []
    for name in os.listdir(base_dir):
        full_path = os.path.join(base_dir, name)
        if os.path.isdir(full_path) and os.path.isdir(os.path.join(full_path, "logs")):
            apps.append((name, os.path.join(full_path, "logs")))
    return apps

# 📊 Read and summarize web APM logs
def summarize_web_apm(log_path):
    try:
        with open(log_path) as f:
            logs = [json.loads(line) for line in f.readlines()[-200:] if '"type": "request"' in line]
        count = len(logs)
        if count == 0:
            return {}

        error_count = sum(1 for l in logs if l.get("status_code", 200) >= 400)
        total_duration = sum(l.get("duration_ms", 0) for l in logs)

        return {
            "Request Count": count,
            "Avg Response Time (ms)": round(total_duration / count, 2),
            "Error Rate (%)": round((error_count / count) * 100, 2)
        }
    except:
        return {}

# 📊 Read and summarize server APM logs
def summarize_server_apm(log_path):
    try:
        with open(log_path) as f:
            last = json.loads(f.readlines()[-1])
        return {
            "CPU (%)": last.get("cpu_percent"),
            "Memory (%)": last.get("memory_percent"),
            "Disk (%)": last.get("disk_percent"),
            "Last Updated": last.get("timestamp")
        }
    except:
        return {}

# 🚀 Endpoint to expose all metrics as JSON
@app.get("/metrics")
def get_metrics():
    summary = {}
    apps = discover_apps(PARENT_DIR)
    for app_name, log_dir in apps:
        web_apm_log = os.path.join(log_dir, "apm_metrics.log")
        server_apm_log = os.path.join(log_dir, "server_metrics.log")

        summary[app_name] = {
            "web_apm": summarize_web_apm(web_apm_log),
            "server_apm": summarize_server_apm(server_apm_log)
        }
    return summary
