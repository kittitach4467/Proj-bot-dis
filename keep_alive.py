from fastapi import FastAPI
import uvicorn
import threading

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "bot is running"}

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()
