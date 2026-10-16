
from fastapi import FastAPI

app = FastAPI(
    title="NeuralDesk AI Research Lab",
    description="NeuralDesk AI research and learning platform",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "project": "NeuralDesk",
        "status": "running",
        "message": "Welcome to NeuralDesk AI research platform DEV!",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
