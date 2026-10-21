
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.tasks.tasks import router as taskrouter
from app.api.routes.auth.auth import router as authrouter
from app.api.routes.subtasks.subtask import router as subtaskrouter
app = FastAPI(title="First FastAPI App")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(taskrouter, prefix="/api/v1")
app.include_router(authrouter, prefix="/api/v1")
app.include_router(subtaskrouter,prefix="/api/v1")


@app.get("/health", tags=["Health"])
def check_health():
    return {"status": "healthy"}
