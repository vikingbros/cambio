import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    print("Hello World")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=2)
