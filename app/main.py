from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def index():
    return {
        "app": "SaaS Status Monitor",
        "message": "სისტემა მუშაობს გამართულად!",
        "hostname": socket.gethostname()
    }