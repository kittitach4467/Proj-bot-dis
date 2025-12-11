from fastapi import FastAPI
import uvicorn
import threading

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

def run():
    uvicorn.run(
        "keep_alive:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1
    )

def keep_alive():
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
