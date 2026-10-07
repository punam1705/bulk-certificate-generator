from fastapi import FastAPI

from .database import engine, Base
from .routes import jobs, certificates


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator API",
    version="1.0.0"
)


app.include_router(jobs.router)
app.include_router(certificates.router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API"
    }