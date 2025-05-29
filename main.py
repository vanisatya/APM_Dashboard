from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Serve static files (like Dashboard.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML dashboard as home page
@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

# Helper: Read last N lines as JSON from a log file
def read_last_json_lines(filepath, count=1):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            return [json.loads(line) for line in lines[-count:]]
    except:
        return []

# Expose combined APM metrics for App1, App2, App3
@app.get("/metrics")
def get_all_app_metrics():
    return {
        "App1": {
            "server": read_last_json_lines("/home/VaniSatya/Web-Application/server_apm1.log", 1),
            "web": read_last_json_lines("/home/VaniSatya/Web-Application/app1.log", 1)
        },
        "App2": {
            "server": read_last_json_lines("/home/VaniSatya/Web-Application-1/server_apm2.log", 1),
            "web": read_last_json_lines("/home/VaniSatya/Web-Application-1/app2.log", 1)
        },
        "App3": {
            "server": read_last_json_lines("/home/VaniSatya/Web-Application-2/server_apm3.log", 1),
            "web": read_last_json_lines("/home/VaniSatya/Web-Application-2/app3.log", 1)
        }
    }
