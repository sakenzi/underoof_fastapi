import uvicorn
from main import app


if __name__ == "__main__":
    # uvicorn.run(app, host="localhost", port=8000, reload=True)
    uvicorn.run("main:app", host="192.168.8.104", port=8000, reload=True)