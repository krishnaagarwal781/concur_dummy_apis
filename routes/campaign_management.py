from fastapi import APIRouter, HTTPException
from models.models import Campaign, UpdateCampaign, CampaignAnalytics, CampaignInsights, ExportCampaignData, ImportCampaignData
from config.database import db
from bson import ObjectId
from datetime import datetime

campaign_router = APIRouter()

@campaign_router.post("/create-campaign", tags=["Campaign Management"])
async def create_campaign(campaign: Campaign):
    result = await db["campaigns"].insert_one(campaign.dict())
    return {"id": str(result.inserted_id)}

@campaign_router.get("/view-campaign/{campaign_id}", tags=["Campaign Management"])
async def view_campaign(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    campaign = await db["campaigns"].find_one({"_id": ObjectId(campaign_id)})
    if campaign:
        return campaign
    raise HTTPException(status_code=404, detail="Campaign not found")

@campaign_router.put("/update-campaign/{campaign_id}", tags=["Campaign Management"])
async def update_campaign(campaign_id: str, campaign: UpdateCampaign):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    result = await db["campaigns"].update_one({"_id": ObjectId(campaign_id)}, {"$set": campaign.dict(exclude_unset=True)})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@campaign_router.put("/publish-campaign/{campaign_id}", tags=["Campaign Management"])
async def publish_campaign(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    result = await db["campaigns"].update_one({"_id": ObjectId(campaign_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@campaign_router.put("/unpublish-campaign/{campaign_id}", tags=["Campaign Management"])
async def unpublish_campaign(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    result = await db["campaigns"].update_one({"_id": ObjectId(campaign_id)}, {"$set": {"status": "unpublished"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@campaign_router.get("/get-all-campaign", tags=["Campaign Management"])
async def get_all_campaigns():
    campaigns = await db["campaigns"].find().to_list(100)
    return campaigns

@campaign_router.get("/get-campaign-analytics/{campaign_id}", tags=["Campaign Management"])
async def get_campaign_analytics(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    # Dummy analytics response
    return {"campaign_id": campaign_id, "total_engagements": 500, "conversion_rate": 5.5}

@campaign_router.delete("/delete-campaign/{campaign_id}", tags=["Campaign Management"])
async def delete_campaign(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    result = await db["campaigns"].delete_one({"_id": ObjectId(campaign_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@campaign_router.post("/schedule-campaign/{campaign_id}", tags=["Campaign Management"])
async def schedule_campaign(campaign_id: str, schedule_time: datetime):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    result = await db["campaigns"].update_one({"_id": ObjectId(campaign_id)}, {"$set": {"schedule_time": schedule_time}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@campaign_router.post("/export-campaign-data/{campaign_id}", tags=["Campaign Management"])
async def export_campaign_data(campaign_id: str, export_data: ExportCampaignData):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    # Dummy export logic
    return {"status": "success", "format": export_data.format}

@campaign_router.post("/import-campaign-data", tags=["Campaign Management"])
async def import_campaign_data(import_data: ImportCampaignData):
    # Dummy import logic
    return {"status": "success"}

@campaign_router.get("/campaign-insights/{campaign_id}", tags=["Campaign Management"])
async def campaign_insights(campaign_id: str):
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    # Dummy insights response
    return {"campaign_id": campaign_id, "insights": {"performance_score": 85, "engagement_rate": 12.3}}
