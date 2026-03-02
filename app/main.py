from fastapi import FastAPI
from api.v1.auth import router as auth_router

app = FastAPI(title="Sonar Vault")

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
