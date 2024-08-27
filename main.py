from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    app_management,
    collection_point_management,
    data_principal_persona,
    data_principal,
    model_notice,
)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to backend"}


app.include_router(app_management.app_management_router)
app.include_router(collection_point_management.collection_router)
app.include_router(data_principal_persona.data_principal_persona_router)
app.include_router(data_principal.data_principal_router)
app.include_router(model_notice.modelNotice)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
