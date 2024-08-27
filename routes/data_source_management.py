from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.models import DataSource, UpdateDataSource
from config.database import db
from bson import ObjectId
import json
import csv

data_source_router = APIRouter()

@data_source_router.post("/create-data-source", tags=["Data Source Management"])
async def create_data_source(source: DataSource):
    result = await db["data_sources"].insert_one(source.dict())
    return {"id": str(result.inserted_id)}

@data_source_router.get("/view-data-source/{source_id}", tags=["Data Source Management"])
async def view_data_source(source_id: str):
    if not ObjectId.is_valid(source_id):
        raise HTTPException(status_code=400, detail="Invalid data source ID")
    source = await db["data_sources"].find_one({"_id": ObjectId(source_id)})
    if source:
        return source
    raise HTTPException(status_code=404, detail="Data source not found")

@data_source_router.put("/update-data-source/{source_id}", tags=["Data Source Management"])
async def update_data_source(source_id: str, source: UpdateDataSource):
    if not ObjectId.is_valid(source_id):
        raise HTTPException(status_code=400, detail="Invalid data source ID")
    result = await db["data_sources"].update_one({"_id": ObjectId(source_id)}, {"$set": source.dict(exclude_unset=True)})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data source not found")

@data_source_router.delete("/delete-data-source/{source_id}", tags=["Data Source Management"])
async def delete_data_source(source_id: str):
    if not ObjectId.is_valid(source_id):
        raise HTTPException(status_code=400, detail="Invalid data source ID")
    result = await db["data_sources"].delete_one({"_id": ObjectId(source_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data source not found")

@data_source_router.get("/list-data-sources", tags=["Data Source Management"])
async def list_data_sources():
    sources = await db["data_sources"].find().to_list(100)
    return sources

@data_source_router.get("/search-data-source", tags=["Data Source Management"])
async def search_data_source(
    name: Optional[str] = Query(None, description="Name of the data source"),
    type: Optional[str] = Query(None, description="Type of the data source"),
    status: Optional[str] = Query(None, description="Status of the data source")
):
    query = {}
    if name:
        query["name"] = name
    if type:
        query["type"] = type
    if status:
        query["status"] = status

    sources = await db["data_sources"].find(query).to_list(100)
    return sources

@data_source_router.put("/archive-data-source/{source_id}", tags=["Data Source Management"])
async def archive_data_source(source_id: str):
    if not ObjectId.is_valid(source_id):
        raise HTTPException(status_code=400, detail="Invalid data source ID")
    result = await db["data_sources"].update_one({"_id": ObjectId(source_id)}, {"$set": {"status": "archived"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data source not found")

@data_source_router.post("/export-data-source", tags=["Data Source Management"])
async def export_data_source(format: str = Query("json", description="Format to export the data (json, csv)")):
    sources = await db["data_sources"].find().to_list(100)
    if format == "json":
        return sources
    elif format == "csv":
        response = []
        for source in sources:
            response.append(source)
        output = []
        for source in response:
            output.append({**source, "_id": str(source["_id"])})
        csv_data = io.StringIO()
        writer = csv.DictWriter(csv_data, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)
        return Response(content=csv_data.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data_sources.csv"})
    raise HTTPException(status_code=400, detail="Unsupported format")

@data_source_router.post("/import-data-source", tags=["Data Source Management"])
async def import_data_source(file: UploadFile):
    if file.content_type == "application/json":
        data = json.load(file.file)
        result = await db["data_sources"].insert_many(data)
        return {"inserted_ids": [str(id) for id in result.inserted_ids]}
    elif file.content_type == "text/csv":
        csv_data = pd.read_csv(file.file)
        data = csv_data.to_dict(orient="records")
        result = await db["data_sources"].insert_many(data)
        return {"inserted_ids": [str(id) for id in result.inserted_ids]}
    raise HTTPException(status_code=400, detail="Unsupported file type")

@data_source_router.post("/validate-data-source/{source_id}", tags=["Data Source Management"])
async def validate_data_source(source_id: str):
    if not ObjectId.is_valid(source_id):
        raise HTTPException(status_code=400, detail="Invalid data source ID")
    # Dummy validation response
    return {"source_id": source_id, "status": "valid"}

@data_source_router.post("/sync-data-source/{source_id}", tags=["Data Source Management"])
async def sync_data_source(source_id: str):
    if not ObjectId.is_valid(source_id):
        raise HTTPException(status_code=400, detail="Invalid data source ID")
    # Dummy synchronization response
    return {"source_id": source_id, "status": "synchronized"}
