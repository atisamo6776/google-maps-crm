"""
FastAPI main application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.models.database import init_db
from app.routes import auth, dashboard, search, companies, admin, excel, config, theme
import os

# Veritabanını başlat
init_db()

# FastAPI app oluştur
app = FastAPI(
    title="Google Maps CRM API",
    description="İşletme arama ve CRM sistemi",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain'ler ekle
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(search.router)
app.include_router(companies.router)
app.include_router(admin.router)
app.include_router(excel.router)
app.include_router(config.router)
app.include_router(theme.router)


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


# Frontend static files ve templates
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")
    templates = Jinja2Templates(directory=os.path.join(frontend_path, "templates"))
    
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard_page(request: Request):
        return templates.TemplateResponse("dashboard.html", {"request": request})
    
    @app.get("/search", response_class=HTMLResponse)
    async def search_page(request: Request):
        return templates.TemplateResponse("search.html", {"request": request})
    
    @app.get("/companies", response_class=HTMLResponse)
    async def companies_page(request: Request):
        return templates.TemplateResponse("companies.html", {"request": request})
    
    @app.get("/admin", response_class=HTMLResponse)
    async def admin_page(request: Request):
        return templates.TemplateResponse("admin.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

