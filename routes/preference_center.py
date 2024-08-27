from fastapi import APIRouter, HTTPException, UploadFile
from models.models import DataPrincipal, UserPreference, PreferenceHistory, ConsentArtifact, PreferenceDataExport
from config.database import db
from bson import ObjectId
from datetime import datetime
from typing import List, Dict

preference_centre_router = APIRouter()

@preference_centre_router.post("/validate-dp", tags=["Preference Centre"])
async def validate_dp(dp: DataPrincipal):
    # Logic to validate data principal
    return {"status": "data principal validated"}

@preference_centre_router.get("/get-dp-consents/{user_id}", tags=["Preference Centre"])
async def get_dp_consents(user_id: str):
    consents = await db["user_preferences"].find_one({"user_id": user_id}, {"consents": 1, "_id": 0})
    if consents:
        return consents
    raise HTTPException(status_code=404, detail="User consents not found")

@preference_centre_router.get("/list-preferences", tags=["Preference Centre"])
async def list_preferences():
    preferences = await db["user_preferences"].find().to_list(100)
    return preferences

@preference_centre_router.post("/revoke-consent", tags=["Preference Centre"])
async def revoke_consent(user_id: str, consent_type: str):
    result = await db["user_preferences"].update_one(
        {"user_id": user_id},
        {"$set": {f"consents.{consent_type}": False}}
    )
    if result.matched_count:
        return {"status": "consent revoked"}
    raise HTTPException(status_code=404, detail="User not found")

@preference_centre_router.post("/enable-consent", tags=["Preference Centre"])
async def enable_consent(user_id: str, consent_type: str):
    result = await db["user_preferences"].update_one(
        {"user_id": user_id},
        {"$set": {f"consents.{consent_type}": True}}
    )
    if result.matched_count:
        return {"status": "consent enabled"}
    raise HTTPException(status_code=404, detail="User not found")

@preference_centre_router.get("/get-dp-artifacts/{user_id}", tags=["Preference Centre"])
async def get_dp_artifacts(user_id: str):
    artifacts = await db["consent_artifacts"].find({"user_id": user_id}).to_list(100)
    if artifacts:
        return artifacts
    raise HTTPException(status_code=404, detail="Consent artifacts not found")

@preference_centre_router.get("/download-consent-artifacts/{artifact_id}", tags=["Preference Centre"])
async def download_consent_artifacts(artifact_id: str):
    artifact = await db["consent_artifacts"].find_one({"artifact_id": artifact_id})
    if artifact:
        return artifact
    raise HTTPException(status_code=404, detail="Artifact not found")

@preference_centre_router.put("/update-preferences/{user_id}", tags=["Preference Centre"])
async def update_preferences(user_id: str, preferences: UserPreference):
    preferences.updated_at = datetime.utcnow()
    result = await db["user_preferences"].update_one({"user_id": user_id}, {"$set": preferences.dict(exclude_unset=True)})
    if result.matched_count:
        return {"status": "preferences updated"}
    raise HTTPException(status_code=404, detail="User not found")

@preference_centre_router.get("/get-preference-history/{user_id}", tags=["Preference Centre"])
async def get_preference_history(user_id: str):
    history = await db["preference_history"].find_one({"user_id": user_id})
    if history:
        return history
    raise HTTPException(status_code=404, detail="Preference history not found")

@preference_centre_router.post("/export-preference-data", tags=["Preference Centre"])
async def export_preference_data(user_id: str, export_format: str):
    preferences = await db["user_preferences"].find_one({"user_id": user_id})
    if preferences:
        data_export = PreferenceDataExport(user_id=user_id, export_format=export_format, data=[preferences])
        # Logic to convert data to the desired export format
        return {"data": data_export}
    raise HTTPException(status_code=404, detail="User not found")

@preference_centre_router.post("/validate-preference", tags=["Preference Centre"])
async def validate_preference(preferences: UserPreference):
    # Logic to validate user preferences and consents
    return {"status": "preferences validated"}
