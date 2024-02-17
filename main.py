from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from elements.user.routers import user_router

app = FastAPI(title="All_BAG")
main_router = APIRouter()
main_router.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(main_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="127.0.0.1", port=8000)