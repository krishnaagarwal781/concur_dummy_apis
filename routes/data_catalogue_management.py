from fastapi import APIRouter, HTTPException
from typing import List
from models.models import DataCatalogue, UpdateDataCatalogue
from config.database import db
from bson import ObjectId

catalogue_router = APIRouter()


@catalogue_router.get("/data-catalogue-dashboard", tags=["Data Catalogue Management"])
async def data_catalogue_dashboard():
    # Dashboard response with a summary of data catalogues (e.g., total active catalogues, etc.)
    total_catalogues = await db["data_catalogues"].count_documents({})
    active_catalogues = await db["data_catalogues"].count_documents(
        {"status": "active"}
    )
    return {
        "total_catalogues": total_catalogues,
        "active_catalogues": active_catalogues,
    }


@catalogue_router.get("/get-data-catalogue", tags=["Data Catalogue Management"])
async def get_data_catalogue():
    # Returns a template for creating a new data catalogue
    return DataCatalogue.schema()


@catalogue_router.post("/create-data-catalogue", tags=["Data Catalogue Management"])
async def create_data_catalogue(data_catalogue: DataCatalogue):
    result = await db["data_catalogues"].insert_one(data_catalogue.dict())
    return {"id": str(result.inserted_id)}


@catalogue_router.get(
    "/view-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def view_data_catalogue(catalogue_id: str):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    catalogue = await db["data_catalogues"].find_one({"_id": ObjectId(catalogue_id)})
    if catalogue:
        return catalogue
    raise HTTPException(status_code=404, detail="Data catalogue not found")


@catalogue_router.put(
    "/update-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def update_data_catalogue(catalogue_id: str, data_catalogue: UpdateDataCatalogue):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    update_dict = data_catalogue.dict(exclude_unset=True)
    result = await db["data_catalogues"].update_one(
        {"_id": ObjectId(catalogue_id)}, {"$set": update_dict}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data catalogue not found")


@catalogue_router.put(
    "/publish-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def publish_data_catalogue(catalogue_id: str):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    result = await db["data_catalogues"].update_one(
        {"_id": ObjectId(catalogue_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data catalogue not found")


@catalogue_router.put(
    "/unpublish-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def unpublish_data_catalogue(catalogue_id: str):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    result = await db["data_catalogues"].update_one(
        {"_id": ObjectId(catalogue_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data catalogue not found")


@catalogue_router.get("/list-data-catalogues", tags=["Data Catalogue Management"])
async def list_data_catalogues():
    catalogues = await db["data_catalogues"].find().to_list(100)
    return catalogues


@catalogue_router.delete(
    "/delete-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def delete_data_catalogue(catalogue_id: str):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    result = await db["data_catalogues"].delete_one({"_id": ObjectId(catalogue_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data catalogue not found")


@catalogue_router.post(
    "/export-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def export_data_catalogue(catalogue_id: str, format: str = "json"):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    catalogue = await db["data_catalogues"].find_one({"_id": ObjectId(catalogue_id)})
    if not catalogue:
        raise HTTPException(status_code=404, detail="Data catalogue not found")

    # Dummy export logic based on the format
    if format == "json":
        return {"data": catalogue}
    elif format == "csv":
        # Convert to CSV format
        return {"data": "CSV format not implemented"}
    elif format == "xml":
        # Convert to XML format
        return {"data": "XML format not implemented"}
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")


@catalogue_router.post("/import-data-catalogue", tags=["Data Catalogue Management"])
async def import_data_catalogue(file: str):
    # Dummy import logic
    return {"status": "Data catalogue imported"}


@catalogue_router.get("/search-data-catalogue", tags=["Data Catalogue Management"])
async def search_data_catalogue(query: str):
    # Dummy search logic
    catalogues = (
        await db["data_catalogues"].find({"entries": {"$regex": query}}).to_list(100)
    )
    return catalogues


@catalogue_router.put(
    "/sync-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def sync_data_catalogue(catalogue_id: str):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    # Dummy sync response
    return {"status": "Data catalogue synchronized", "catalogue_id": catalogue_id}


@catalogue_router.post(
    "/categorize-data-catalogue/{catalogue_id}", tags=["Data Catalogue Management"]
)
async def categorize_data_catalogue(catalogue_id: str, categories: List[str]):
    if not ObjectId.is_valid(catalogue_id):
        raise HTTPException(status_code=400, detail="Invalid catalogue ID")
    result = await db["data_catalogues"].update_one(
        {"_id": ObjectId(catalogue_id)}, {"$set": {"categories": categories}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data catalogue not found")
