import uvicorn
from fastapi import FastAPI

from app.database import create_pool
from app.initial_setup import create_locations, create_trucks
from app.routers import router as cargo_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():

    pool = create_pool()
    async with pool() as db:
        await create_locations(db)
        await create_trucks(db)

app.include_router(cargo_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
