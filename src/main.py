import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from routes import router


class Config:
    atlas_uri: str = "mongodb+srv://cambio:cambio@cambio.o9wq6.mongodb.net/?retryWrites=true&w=majority"
    db_name: str = "cambio"


config = Config()
app = FastAPI()

app.include_router(router)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config.atlas_uri, server_api=ServerApi("1"))
    app.database = app.mongodb_client[config.db_name]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Connection to MongoDB closed!")


def main():
    print("Hello World")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=2)
