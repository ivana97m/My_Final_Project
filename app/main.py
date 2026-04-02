from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.api.routers.projects import router as project_router
from app.db.session import init_db
app = FastAPI()

#@asynccontextmanager
#async def lifespan(app: FastAPI):
    # pri svakom startu aplikacije kreira tabele u bazi ako ne postoje
    #await init_db()
    #yield
@app.get("/health")
def health():
    return {"status": "ok"}



app.include_router(auth_router)
app.include_router(project_router)