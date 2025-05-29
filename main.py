from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Serve static files like dashboard.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML dashboard at the root URL
@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

# Return latest metrics (last 3 lines assumed to be App1, App2, App3)
@app.get("/metrics")
def get_metrics():
    log_file = "/home/VaniSatya/logs/server_metrics.log"  # Update path if different
    if not os.path.exists(log_file):
        return {"metrics": []}

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            # Assuming last 3 lines are from App1, App2, App3 (update logic as needed)
            last_lines = lines[-3:]
            metrics = [json.loads(line) for line in last_lines]
        return {"metrics": metrics}
    except Exception as e:
        return {"metrics": [], "error": str(e)}
