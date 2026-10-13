from fastapi import FastAPI,HTTPException,status
from app.api.routes.tasks.tasks import router as taskrouter
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI(title="First FastAPI App")

app.include_router(
    taskrouter,
    prefix="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)

@app.get("/health",tags=["Health"])
def checkHealth():
    return {"status":"healthy"}




