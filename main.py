from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from models import *
from database import engine, SessionLocal
from routers import auth, facebook, leads, templates
import uvicorn

app = FastAPI(title="Facebook Leads Analysis System")

# יצירת הטבלאות בבסיס הנתונים
Base.metadata.create_all(bind=engine)

# הגדרת CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# הוספת הראוטרים
app.include_router(auth.router)
app.include_router(facebook.router)
app.include_router(leads.router)
app.include_router(templates.router)

# שירות קבצים סטטיים (עבור הדשבורד)
app.mount("/static", StaticFiles(directory="frontend/build"), name="static")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """שירות קבצי Frontend"""
    file_path = f"frontend/build/{full_path}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("frontend/build/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)), reload=True)
