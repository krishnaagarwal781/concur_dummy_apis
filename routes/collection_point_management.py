from fastapi import APIRouter, HTTPException
from models.models import CollectionPoint, UpdateCollectionPoint
from config.database import db
from bson import ObjectId

collection_router = APIRouter()

@collection_router.post("/create-collection-point", tags=["Collection Point Management"])
async def create_collection_point(point: CollectionPoint):
    result = await db["collection_points"].insert_one(point.dict())
    return {"id": str(result.inserted_id)}

@collection_router.get("/get-collection-point", tags=["Collection Point Management"])
async def get_collection_point():
    points = await db["collection_points"].find().to_list(100)
    return points

@collection_router.get("/collection-point-details/{point_id}", tags=["Collection Point Management"])
async def collection_point_details(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    point = await db["collection_points"].find_one({"_id": ObjectId(point_id)})
    if point:
        return point
    raise HTTPException(status_code=404, detail="Collection point not found")

@collection_router.get("/collection-point-analytics/{point_id}", tags=["Collection Point Management"])
async def collection_point_analytics(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    # Dummy analytics response
    return {"point_id": point_id, "total_data": 1000, "processed_data": 800}

@collection_router.put("/update-collection-point/{point_id}", tags=["Collection Point Management"])
async def update_collection_point(point_id: str, point: UpdateCollectionPoint):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one({"_id": ObjectId(point_id)}, {"$set": point.dict(exclude_unset=True)})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")

@collection_router.put("/publish-collection-point/{point_id}", tags=["Collection Point Management"])
async def publish_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one({"_id": ObjectId(point_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")

@collection_router.put("/unpublish-collection-point/{point_id}", tags=["Collection Point Management"])
async def unpublish_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one({"_id": ObjectId(point_id)}, {"$set": {"status": "unpublished"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")
