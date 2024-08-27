from fastapi import APIRouter, HTTPException
from models.models import App, UpdateApp
from config.database import db
from bson import ObjectId

app_management_router = APIRouter()


@app_management_router.post("/register-app", tags=["App Management"])
async def register_app(app: App):
    result = await db["apps"].insert_one(app.dict())
    return {"id": str(result.inserted_id)}


@app_management_router.get("/get-app-list", tags=["App Management"])
async def get_app_list():
    apps = await db["apps"].find().to_list(100)
    return apps


@app_management_router.put("/update-app/{app_id}", tags=["App Management"])
async def update_app(app_id: str, app: UpdateApp):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": app.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")


@app_management_router.put("/publish-app/{app_id}", tags=["App Management"])
async def publish_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")


@app_management_router.put("/unpublish-app/{app_id}", tags=["App Management"])
async def unpublish_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")
