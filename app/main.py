from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.v1.auth import router as auth_router, get_current_active_user

app = FastAPI(title="Sonar Vault")

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
async def serve_root():
    """Serves the index.html which handles client-side redirection based on auth."""
    return FileResponse("frontend/index.html")

@app.get("/login")
async def serve_login():
    """Serves the login page."""
    return FileResponse("frontend/login.html")

@app.get("/register")
async def serve_register():
    """Serves the registration page."""
    return FileResponse("frontend/register.html")

@app.get("/users")
async def serve_users():
    """Serves the user management page."""
    return FileResponse("frontend/users.html")

@app.get("/dashboard")
async def serve_dashboard():
    """Serves the dashboard page."""
    return FileResponse("frontend/dashboard.html")

# Serve frontend static files
# We mount this last so it doesn't override our explicit routes
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

