from fastapi import APIRouter, HTTPException
from typing import List
from models.models import ScanProfile, UpdateScanProfile
from config.database import db
from bson import ObjectId

profile_router = APIRouter()

@profile_router.get("/scan-profile-dashboard", tags=["Scan Profile Management"])
async def scan_profile_dashboard():
    # Dashboard response with a summary of scan profiles (e.g., total active profiles, etc.)
    total_profiles = await db["scan_profiles"].count_documents({})
    active_profiles = await db["scan_profiles"].count_documents({"status": "active"})
    return {"total_profiles": total_profiles, "active_profiles": active_profiles}

@profile_router.get("/get-scan-profile-template", tags=["Scan Profile Management"])
async def get_scan_profile_template():
    # Returns a template for creating a new scan profile
    return ScanProfile.schema()

@profile_router.post("/create-scan-profile", tags=["Scan Profile Management"])
async def create_scan_profile(scan_profile: ScanProfile):
    result = await db["scan_profiles"].insert_one(scan_profile.dict())
    return {"id": str(result.inserted_id)}

@profile_router.get("/view-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def view_scan_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    profile = await db["scan_profiles"].find_one({"_id": ObjectId(profile_id)})
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Scan profile not found")

@profile_router.put("/update-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def update_scan_profile(profile_id: str, scan_profile: UpdateScanProfile):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    update_dict = scan_profile.dict(exclude_unset=True)
    result = await db["scan_profiles"].update_one({"_id": ObjectId(profile_id)}, {"$set": update_dict})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Scan profile not found")

@profile_router.put("/publish-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def publish_scan_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    result = await db["scan_profiles"].update_one({"_id": ObjectId(profile_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Scan profile not found")

@profile_router.put("/unpublish-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def unpublish_scan_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    result = await db["scan_profiles"].update_one({"_id": ObjectId(profile_id)}, {"$set": {"status": "unpublished"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Scan profile not found")

@profile_router.get("/list-scan-profiles", tags=["Scan Profile Management"])
async def list_scan_profiles():
    profiles = await db["scan_profiles"].find().to_list(100)
    return profiles

@profile_router.delete("/delete-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def delete_scan_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    result = await db["scan_profiles"].delete_one({"_id": ObjectId(profile_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Scan profile not found")

@profile_router.post("/duplicate-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def duplicate_scan_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    profile = await db["scan_profiles"].find_one({"_id": ObjectId(profile_id)})
    if not profile:
        raise HTTPException(status_code=404, detail="Scan profile not found")
    
    # Remove _id to create a new profile
    profile.pop("_id")
    result = await db["scan_profiles"].insert_one(profile)
    return {"id": str(result.inserted_id)}

@profile_router.post("/execute-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def execute_scan_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    # Dummy execution response
    return {"status": "Scan executed", "profile_id": profile_id}

@profile_router.post("/schedule-scan-profile/{profile_id}", tags=["Scan Profile Management"])
async def schedule_scan_profile(profile_id: str, schedule_time: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    # Dummy schedule response
    return {"status": "Scan profile scheduled", "profile_id": profile_id, "schedule_time": schedule_time}

@profile_router.get("/scan-profile-logs/{profile_id}", tags=["Scan Profile Management"])
async def scan_profile_logs(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")
    # Dummy logs response
    return {"profile_id": profile_id, "logs": []}
