from fastapi import APIRouter, HTTPException
from models.models import (
    ReconsentRule,
    ReconsentDetails,
    ReconsentInsights,
    ReconsentAudit,
)
from config.database import db
from bson import ObjectId
from datetime import datetime
from typing import List, Dict

reconsent_router = APIRouter()


@reconsent_router.get("/reconsent-dashboard", tags=["Reconsent Management"])
async def reconsent_dashboard():
    # Placeholder for dashboard data
    return {"message": "Reconsent dashboard data"}


@reconsent_router.get("/reconsent-analytics", tags=["Reconsent Management"])
async def reconsent_analytics():
    # Placeholder for analytics data
    return {"message": "Reconsent analytics data"}


@reconsent_router.get("/reconsent-status/{rule_id}", tags=["Reconsent Management"])
async def reconsent_status(rule_id: str):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    status = await db["reconsent"].find_one(
        {"rule_id": rule_id}, {"status": 1, "_id": 0}
    )
    if status:
        return status
    raise HTTPException(status_code=404, detail="Reconsent rule not found")


@reconsent_router.get("/get-reconsent-rule/{rule_id}", tags=["Reconsent Management"])
async def get_reconsent_rule(rule_id: str):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    rule = await db["reconsent_rules"].find_one({"_id": ObjectId(rule_id)})
    if rule:
        return rule
    raise HTTPException(status_code=404, detail="Reconsent rule not found")


@reconsent_router.post("/create-reconsent-rule", tags=["Reconsent Management"])
async def create_reconsent_rule(rule: ReconsentRule):
    rule.created_at = datetime.utcnow()
    rule.updated_at = datetime.utcnow()
    result = await db["reconsent_rules"].insert_one(rule.dict())
    return {"id": str(result.inserted_id)}


@reconsent_router.put("/update-reconsent-rule/{rule_id}", tags=["Reconsent Management"])
async def update_reconsent_rule(rule_id: str, rule: ReconsentRule):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    rule.updated_at = datetime.utcnow()
    result = await db["reconsent_rules"].update_one(
        {"_id": ObjectId(rule_id)}, {"$set": rule.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Reconsent rule not found")


@reconsent_router.put(
    "/publish-reconsent-rule/{rule_id}", tags=["Reconsent Management"]
)
async def publish_reconsent_rule(rule_id: str):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    result = await db["reconsent_rules"].update_one(
        {"_id": ObjectId(rule_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Reconsent rule not found")


@reconsent_router.put(
    "/unpublish-reconsent-rule/{rule_id}", tags=["Reconsent Management"]
)
async def unpublish_reconsent_rule(rule_id: str):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    result = await db["reconsent_rules"].update_one(
        {"_id": ObjectId(rule_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Reconsent rule not found")


@reconsent_router.post("/bulk-upload-reconsent", tags=["Reconsent Management"])
async def bulk_upload_reconsent(file: UploadFile):
    # Logic to handle bulk upload of reconsent data
    return {"status": "bulk upload processed"}


@reconsent_router.get("/bulk-download-reconsent", tags=["Reconsent Management"])
async def bulk_download_reconsent():
    # Logic to handle bulk download of reconsent data
    return {"data": "bulk download data"}


@reconsent_router.get("/list-reconsent-rules", tags=["Reconsent Management"])
async def list_reconsent_rules():
    rules = await db["reconsent_rules"].find().to_list(100)
    return rules


@reconsent_router.delete(
    "/delete-reconsent-rule/{rule_id}", tags=["Reconsent Management"]
)
async def delete_reconsent_rule(rule_id: str):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    result = await db["reconsent_rules"].delete_one({"_id": ObjectId(rule_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Reconsent rule not found")


@reconsent_router.post("/schedule-reconsent", tags=["Reconsent Management"])
async def schedule_reconsent(schedule_time: datetime, rule_id: str):
    # Logic to schedule reconsent requests
    return {
        "status": "reconsent scheduled",
        "schedule_time": schedule_time,
        "rule_id": rule_id,
    }


@reconsent_router.get(
    "/view-reconsent-details/{rule_id}", tags=["Reconsent Management"]
)
async def view_reconsent_details(rule_id: str):
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=400, detail="Invalid rule ID")
    details = await db["reconsent"].find_one({"rule_id": rule_id})
    if details:
        return details
    raise HTTPException(status_code=404, detail="Reconsent details not found")


@reconsent_router.get("/reconsent-insights", tags=["Reconsent Management"])
async def reconsent_insights():
    # Placeholder for reconsent insights
    return {"message": "Reconsent insights data"}


@reconsent_router.get("/reconsent-audit", tags=["Reconsent Management"])
async def reconsent_audit():
    # Placeholder for reconsent audit data
    return {"status": "audit complete"}


@reconsent_router.post("/validate-reconsent-rule", tags=["Reconsent Management"])
async def validate_reconsent_rule(rule: ReconsentRule):
    # Logic to validate a reconsent rule
    return {"status": "rule is valid"}
