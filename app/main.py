from fastapi import FastAPI
from app.api.telegrams import router as telegram_router

app = FastAPI()

app.include_router(telegram_router, prefix="/api/v1", tags=["Telegram"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
