from fastapi import APIRouter, HTTPException
from models.models import (
    Consent,
    ConsentArtifact,
    ConsentHistory,
    ConsentInsights,
    BulkUploadConsents,
    ConsentReport,
)
from config.database import db
from bson import ObjectId
from typing import List, Optional
import csv
import io

consent_router = APIRouter()


@consent_router.get("/get-all-consents", tags=["Consent Management"])
async def get_all_consents():
    consents = await db["consents"].find().to_list(100)
    return consents


@consent_router.get("/get-consent-artifact/{consent_id}", tags=["Consent Management"])
async def get_consent_artifact(consent_id: str):
    if not ObjectId.is_valid(consent_id):
        raise HTTPException(status_code=400, detail="Invalid consent ID")
    artifact = await db["consent_artifacts"].find_one({"consent_id": consent_id})
    if artifact:
        return artifact
    raise HTTPException(status_code=404, detail="Consent artifact not found")


@consent_router.get("/get-consent-history/{user_id}", tags=["Consent Management"])
async def get_consent_history(user_id: str):
    history = await db["consent_history"].find_one({"user_id": user_id})
    if history:
        return history
    raise HTTPException(status_code=404, detail="Consent history not found")


@consent_router.get("/get-consent-insights/{user_id}", tags=["Consent Management"])
async def get_consent_insights(user_id: str):
    insights = await db["consent_insights"].find_one({"user_id": user_id})
    if insights:
        return insights
    raise HTTPException(status_code=404, detail="Consent insights not found")


@consent_router.post("/bulk-download-consents", tags=["Consent Management"])
async def bulk_download_consents():
    consents = await db["consents"].find().to_list(100)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=consents[0].keys())
    writer.writeheader()
    for consent in consents:
        writer.writerow(consent)
    output.seek(0)
    return {"data": output.getvalue()}


@consent_router.post("/bulk-upload-consents", tags=["Consent Management"])
async def bulk_upload_consents(bulk_upload: BulkUploadConsents):
    if not bulk_upload.consents:
        raise HTTPException(status_code=400, detail="No consent records to upload")
    result = await db["consents"].insert_many(
        [consent.dict() for consent in bulk_upload.consents]
    )
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}


@consent_router.get("/search-consents", tags=["Consent Management"])
async def search_consents(
    date: Optional[str] = None, type: Optional[str] = None, status: Optional[str] = None
):
    query = {}
    if date:
        query["timestamp"] = {"$gte": datetime.fromisoformat(date)}
    if type:
        query["consent_type"] = type
    if status:
        query["status"] = status
    consents = await db["consents"].find(query).to_list(100)
    return consents


@consent_router.post("/sync-consents", tags=["Consent Management"])
async def sync_consents():
    # Dummy sync logic
    return {"status": "success"}


@consent_router.post("/export-consent", tags=["Consent Management"])
async def export_consent(consent_id: str):
    if not ObjectId.is_valid(consent_id):
        raise HTTPException(status_code=400, detail="Invalid consent ID")
    consent = await db["consents"].find_one({"_id": ObjectId(consent_id)})
    if consent:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=consent.keys())
        writer.writeheader()
        writer.writerow(consent)
        output.seek(0)
        return {"data": output.getvalue()}
    raise HTTPException(status_code=404, detail="Consent not found")


@consent_router.post("/import-consent", tags=["Consent Management"])
async def import_consent(consent_data: List[Consent]):
    if not consent_data:
        raise HTTPException(status_code=400, detail="No consent records to import")
    result = await db["consents"].insert_many(
        [consent.dict() for consent in consent_data]
    )
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}


@consent_router.post("/consent-audit", tags=["Consent Management"])
async def consent_audit():
    # Dummy audit logic
    return {"status": "success"}


@consent_router.post("/generate-consent-report/{user_id}", tags=["Consent Management"])
async def generate_consent_report(user_id: str):
    report = await db["consent_reports"].find_one({"user_id": user_id})
    if report:
        return report
    raise HTTPException(status_code=404, detail="Consent report not found")
