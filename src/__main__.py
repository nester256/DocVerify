import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.main:create_app", host="0.0.0.0", port=8000, factory=True, reload=True)
