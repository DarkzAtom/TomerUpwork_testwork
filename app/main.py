from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers import auth_controller, post_controller

app = FastAPI(title="Blog API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_controller.router, tags=["Authentication"])
app.include_router(post_controller.router, tags=["Posts"])

@app.get("/")
async def root():
    # root endpoint health check
    return {"status": "healthy", "message": "Welcome to the Blog API"}
