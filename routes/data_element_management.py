from fastapi import APIRouter, HTTPException
from typing import List
from models.models import DataElement, UpdateDataElement
from config.database import db
from bson import ObjectId

element_router = APIRouter()

@element_router.get("/get-all-data-elements", tags=["Data Element Management"])
async def get_all_data_elements():
    elements = await db["data_elements"].find().to_list(100)
    return elements

@element_router.post("/add-data-element", tags=["Data Element Management"])
async def add_data_element(data_element: DataElement):
    result = await db["data_elements"].insert_one(data_element.dict())
    return {"id": str(result.inserted_id)}

@element_router.put("/update-data-element/{element_id}", tags=["Data Element Management"])
async def update_data_element(element_id: str, data_element: UpdateDataElement):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    update_dict = data_element.dict(exclude_unset=True)
    result = await db["data_elements"].update_one({"_id": ObjectId(element_id)}, {"$set": update_dict})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data element not found")

@element_router.put("/publish-data-element/{element_id}", tags=["Data Element Management"])
async def publish_data_element(element_id: str):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    result = await db["data_elements"].update_one({"_id": ObjectId(element_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data element not found")

@element_router.put("/archive-data-element/{element_id}", tags=["Data Element Management"])
async def archive_data_element(element_id: str):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    result = await db["data_elements"].update_one({"_id": ObjectId(element_id)}, {"$set": {"status": "archived"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data element not found")

@element_router.put("/restore-data-element/{element_id}", tags=["Data Element Management"])
async def restore_data_element(element_id: str):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    result = await db["data_elements"].update_one({"_id": ObjectId(element_id)}, {"$set": {"status": "active"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data element not found")

@element_router.get("/view-data-element/{element_id}", tags=["Data Element Management"])
async def view_data_element(element_id: str):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    element = await db["data_elements"].find_one({"_id": ObjectId(element_id)})
    if element:
        return element
    raise HTTPException(status_code=404, detail="Data element not found")

@element_router.get("/list-data-elements", tags=["Data Element Management"])
async def list_data_elements():
    elements = await db["data_elements"].find().to_list(100)
    return elements

@element_router.get("/search-data-element", tags=["Data Element Management"])
async def search_data_element(query: str):
    # Search for data elements by name or description
    elements = await db["data_elements"].find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    }).to_list(100)
    return elements

@element_router.get("/validate-data-element/{element_id}", tags=["Data Element Management"])
async def validate_data_element(element_id: str):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    element = await db["data_elements"].find_one({"_id": ObjectId(element_id)})
    if element:
        # Dummy validation logic
        return {"status": "valid", "data_element": element}
    raise HTTPException(status_code=404, detail="Data element not found")

@element_router.put("/sync-data-element/{element_id}", tags=["Data Element Management"])
async def sync_data_element(element_id: str):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    # Dummy sync response
    return {"status": "Data element synchronized", "element_id": element_id}

@element_router.post("/categorize-data-element/{element_id}", tags=["Data Element Management"])
async def categorize_data_element(element_id: str, categories: List[str]):
    if not ObjectId.is_valid(element_id):
        raise HTTPException(status_code=400, detail="Invalid data element ID")
    result = await db["data_elements"].update_one({"_id": ObjectId(element_id)}, {"$set": {"categories": categories}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Data element not found")
