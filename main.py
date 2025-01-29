"""
Read this article carefully to get the context how ST_AsMVT Works

https://chatgpt.com/share/6798ac90-08bc-8008-bf2b-96be256cd311
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import crud_api, mvt_api

app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

# Add CORS Policy middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(mvt.router)
app.include_router(crud_api.router)



