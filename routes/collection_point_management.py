from fastapi import APIRouter, HTTPException
from models.models import (
    CollectionPoint,
    UpdateCollectionPoint,
    CollectionPointInsights,
    ExportCollectionPointData,
    ImportCollectionPointData,
    AuditCollectionPoint,
)
from config.database import db
from bson import ObjectId

collection_router = APIRouter()


@collection_router.post(
    "/create-collection-point", tags=["Collection Point Management"]
)
async def create_collection_point(point: CollectionPoint):
    result = await db["collection_points"].insert_one(point.dict())
    return {"id": str(result.inserted_id)}


@collection_router.get("/get-collection-point", tags=["Collection Point Management"])
async def get_collection_point():
    points = await db["collection_points"].find().to_list(100)
    return points


@collection_router.get(
    "/collection-point-details/{point_id}", tags=["Collection Point Management"]
)
async def collection_point_details(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    point = await db["collection_points"].find_one({"_id": ObjectId(point_id)})
    if point:
        return point
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.get(
    "/collection-point-analytics/{point_id}", tags=["Collection Point Management"]
)
async def collection_point_analytics(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    # Dummy analytics response
    return {"point_id": point_id, "total_data": 1000, "processed_data": 800}


@collection_router.put(
    "/update-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def update_collection_point(point_id: str, point: UpdateCollectionPoint):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": point.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.put(
    "/publish-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def publish_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.put(
    "/unpublish-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def unpublish_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.put(
    "/activate-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def activate_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": {"status": "active"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.put(
    "/deactivate-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def deactivate_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": {"status": "inactive"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.post(
    "/duplicate-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def duplicate_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    original = await db["collection_points"].find_one({"_id": ObjectId(point_id)})
    if original:
        duplicate = original.copy()
        duplicate["_id"] = ObjectId()
        result = await db["collection_points"].insert_one(duplicate)
        return {"id": str(result.inserted_id)}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.post(
    "/archive-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def archive_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": {"status": "archived"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.post(
    "/restore-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def restore_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    result = await db["collection_points"].update_one(
        {"_id": ObjectId(point_id)}, {"$set": {"status": "active"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Collection point not found")


@collection_router.post(
    "/validate-collection-point/{point_id}", tags=["Collection Point Management"]
)
async def validate_collection_point(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    # Dummy validation logic
    return {"status": "valid", "point_id": point_id}


@collection_router.get(
    "/collection-point-insights/{point_id}", tags=["Collection Point Management"]
)
async def collection_point_insights(point_id: str):
    if not ObjectId.is_valid(point_id):
        raise HTTPException(status_code=400, detail="Invalid collection point ID")
    # Dummy insights response
    return {
        "point_id": point_id,
        "insights": {"total_data_collected": 1000, "data_processed": 800},
    }


@collection_router.post(
    "/export-collection-point-data", tags=["Collection Point Management"]
)
async def export_collection_point_data(export_data: ExportCollectionPointData):
    # Dummy export logic
    return {"status": "success", "format": export_data.format}


@collection_router.post(
    "/import-collection-point-data", tags=["Collection Point Management"]
)
async def import_collection_point_data(import_data: ImportCollectionPointData):
    # Dummy import logic
    return {"status": "success", "format": import_data.format}


@collection_router.post("/audit-collection-point", tags=["Collection Point Management"])
async def audit_collection_point(audit: AuditCollectionPoint):
    # Dummy audit logic
    return {
        "status": "success",
        "audit_result": audit.audit_result,
        "compliance_status": audit.compliance_status,
    }
