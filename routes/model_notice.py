from fastapi import APIRouter, HTTPException
from models.models import (
    ModelNotice,
    UpdateModelNotice,
    ModelNoticeInsights,
    ExportModelNotice,
    ImportModelNotice,
    SearchModelNotice,
)
from config.database import db
from bson import ObjectId

modelNotice = APIRouter()


@modelNotice.get("/get-model-notice-template", tags=["Model Notice Management"])
async def get_model_notice_template():
    templates = await db["model_notices"].find().to_list(100)
    return templates


@modelNotice.get(
    "/view-model-notice-template/{template_id}", tags=["Model Notice Management"]
)
async def view_model_notice_template(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    template = await db["model_notices"].find_one({"_id": ObjectId(template_id)})
    if template:
        return template
    raise HTTPException(status_code=404, detail="Model notice template not found")


@modelNotice.post("/create-model-notice-template", tags=["Model Notice Management"])
async def create_model_notice_template(template: ModelNotice):
    result = await db["model_notices"].insert_one(template.dict())
    return {"id": str(result.inserted_id)}


@modelNotice.put(
    "/update-model-notice-template/{template_id}", tags=["Model Notice Management"]
)
async def update_model_notice_template(template_id: str, template: UpdateModelNotice):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    result = await db["model_notices"].update_one(
        {"_id": ObjectId(template_id)}, {"$set": template.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice template not found")


@modelNotice.put(
    "/publish-model-notice/{template_id}", tags=["Model Notice Management"]
)
async def publish_model_notice(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    result = await db["model_notices"].update_one(
        {"_id": ObjectId(template_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice template not found")


@modelNotice.put(
    "/unpublish-model-notice/{template_id}", tags=["Model Notice Management"]
)
async def unpublish_model_notice(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    result = await db["model_notices"].update_one(
        {"_id": ObjectId(template_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice template not found")


@modelNotice.get("/list-model-notices", tags=["Model Notice Management"])
async def list_model_notices():
    notices = await db["model_notices"].find().to_list(100)
    return notices


@modelNotice.delete(
    "/delete-model-notice/{template_id}", tags=["Model Notice Management"]
)
async def delete_model_notice(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    result = await db["model_notices"].delete_one({"_id": ObjectId(template_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice template not found")


@modelNotice.post(
    "/validate-model-notice/{template_id}", tags=["Model Notice Management"]
)
async def validate_model_notice(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    # Dummy validation logic
    return {"status": "valid", "template_id": template_id}


@modelNotice.post("/export-model-notice", tags=["Model Notice Management"])
async def export_model_notice(export_data: ExportModelNotice):
    # Dummy export logic
    return {"status": "success", "format": export_data.format}


@modelNotice.post("/import-model-notice", tags=["Model Notice Management"])
async def import_model_notice(import_data: ImportModelNotice):
    # Dummy import logic
    return {"status": "success", "format": import_data.format}


@modelNotice.post("/search-model-notice", tags=["Model Notice Management"])
async def search_model_notice(search_data: SearchModelNotice):
    query = search_data.query
    filters = search_data.filters or {}
    # Dummy search logic
    return {"status": "success", "results": []}


@modelNotice.get(
    "/model-notice-insights/{template_id}", tags=["Model Notice Management"]
)
async def model_notice_insights(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    # Dummy insights response
    return {"template_id": template_id, "insights": {"views": 100, "engagements": 75}}
