from fastapi import APIRouter, HTTPException
from typing import List
from models.models import DataPrincipal, UpdateDataPrincipal
from config.database import db
from bson import ObjectId

data_principal_router = APIRouter()

@data_principal_router.post("/add-data-principal", tags=["Data Principal Management"])
async def add_data_principal(principal: DataPrincipal):
    result = await db["data_principals"].insert_one(principal.dict())
    return {"id": str(result.inserted_id)}

@data_principal_router.get("/view-data-principal/{principal_id}", tags=["Data Principal Management"])
async def view_data_principal(principal_id: str):
    if not ObjectId.is_valid(principal_id):
        raise HTTPException(status_code=400, detail="Invalid data principal ID")
    principal = await db["data_principals"].find_one({"_id": ObjectId(principal_id)})
    if principal:
        return principal
    raise HTTPException(status_code=404, detail="Data principal not found")

@data_principal_router.get("/data-principal-insights/{principal_id}", tags=["Data Principal Management"])
async def data_principal_insights(principal_id: str):
    if not ObjectId.is_valid(principal_id):
        raise HTTPException(status_code=400, detail="Invalid data principal ID")
    # Dummy insights response
    return {"principal_id": principal_id, "insights": {"total_data": 1000, "active_data": 800}}

@data_principal_router.post("/bulk-import-data-principal", tags=["Data Principal Management"])
async def bulk_import_data_principal(principals: List[DataPrincipal]):
    result = await db["data_principals"].insert_many([principal.dict() for principal in principals])
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

@data_principal_router.get("/bulk-export-data-principal", tags=["Data Principal Management"])
async def bulk_export_data_principal():
    principals = await db["data_principals"].find().to_list(100)
    return principals

@data_principal_router.delete("/delete-data-principal/{principal_id}", tags=["Data Principal Management"])
async def delete_data_principal(principal_id: str):
    if not ObjectId.is_valid(principal_id):
        raise HTTPException(status_code=400, detail="Invalid data principal ID")
    result = await db["data_principals"].delete_one({"_id": ObjectId(principal_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data principal not found")
