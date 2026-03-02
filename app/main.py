from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1.auth import router as auth_router

app = FastAPI(title="Sonar Vault")

app.include_router(auth_router)

# Serve frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/health")
def health_check():
    return {"status": "ok"}
