from fastapi import FastAPI
from app.routes import ingest, agent

app = FastAPI()
app.include_router(ingest.router, prefix="/ingest")
app.include_router(agent.router, prefix="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
