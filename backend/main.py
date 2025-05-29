from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather import router as weather_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Явно указываем origin фронтенда
    allow_credentials=True,
    allow_methods=["*"],                      # Разрешаем все методы
    allow_headers=["*"],                      # Разрешаем все заголовки
)

app.include_router(weather_router)