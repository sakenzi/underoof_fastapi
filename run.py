import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    # uvicorn.run("main:app", host="192.168.8.102", port=8000, reload=True)