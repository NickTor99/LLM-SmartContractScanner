import uvicorn
from api_server.api.routes import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("api_server.entrypoint:app", host="0.0.0.0", port=8000, reload=True)
