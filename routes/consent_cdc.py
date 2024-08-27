from fastapi import APIRouter, HTTPException
from models.models import ConsentCDC, ConsentCDCInsights, ConsentCDCAudit
from config.database import db
from bson import ObjectId
from typing import List, Dict
from datetime import datetime

consent_cdc_router = APIRouter()

@consent_cdc_router.post("/create-consent-cdc", tags=["Consent CDC"])
async def create_consent_cdc(cdc: ConsentCDC):
    result = await db["consent_cdc"].insert_one(cdc.dict())
    return {"id": str(result.inserted_id)}

@consent_cdc_router.get("/list-consent-cdc", tags=["Consent CDC"])
async def list_consent_cdc():
    cdc_records = await db["consent_cdc"].find().to_list(100)
    return cdc_records

@consent_cdc_router.get("/filter-consent-cdc", tags=["Consent CDC"])
async def filter_consent_cdc(
    consent_id: str = None,
    change_type: str = None,
    start_date: str = None,
    end_date: str = None
):
    query = {}
    if consent_id:
        query["consent_id"] = consent_id
    if change_type:
        query["change_type"] = change_type
    if start_date:
        query["change_timestamp"] = {"$gte": datetime.fromisoformat(start_date)}
    if end_date:
        if "change_timestamp" not in query:
            query["change_timestamp"] = {}
        query["change_timestamp"]["$lte"] = datetime.fromisoformat(end_date)
    cdc_records = await db["consent_cdc"].find(query).to_list(100)
    return cdc_records

@consent_cdc_router.get("/get-consent-cdc-update/{cdc_id}", tags=["Consent CDC"])
async def get_consent_cdc_update(cdc_id: str):
    if not ObjectId.is_valid(cdc_id):
        raise HTTPException(status_code=400, detail="Invalid CDC ID")
    cdc_record = await db["consent_cdc"].find_one({"_id": ObjectId(cdc_id)})
    if cdc_record:
        return cdc_record
    raise HTTPException(status_code=404, detail="CDC record not found")

@consent_cdc_router.put("/update-consent-cdc/{cdc_id}", tags=["Consent CDC"])
async def update_consent_cdc(cdc_id: str, cdc: ConsentCDC):
    if not ObjectId.is_valid(cdc_id):
        raise HTTPException(status_code=400, detail="Invalid CDC ID")
    result = await db["consent_cdc"].update_one({"_id": ObjectId(cdc_id)}, {"$set": cdc.dict()})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="CDC record not found")

@consent_cdc_router.delete("/delete-consent-cdc/{cdc_id}", tags=["Consent CDC"])
async def delete_consent_cdc(cdc_id: str):
    if not ObjectId.is_valid(cdc_id):
        raise HTTPException(status_code=400, detail="Invalid CDC ID")
    result = await db["consent_cdc"].delete_one({"_id": ObjectId(cdc_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="CDC record not found")

@consent_cdc_router.get("/consent-cdc-insights", tags=["Consent CDC"])
async def consent_cdc_insights():
    # Example insights calculation
    pipeline = [
        {"$group": {"_id": "$change_type", "count": {"$sum": 1}}},
        {"$group": {"_id": None, "total_changes": {"$sum": "$count"}, "changes_by_type": {"$push": {"type": "$_id", "count": "$count"}}}}
    ]
    insights = await db["consent_cdc"].aggregate(pipeline).to_list(1)
    if insights:
        return insights[0]
    return {"total_changes": 0, "changes_by_type": []}

@consent_cdc_router.get("/consent-cdc-audit", tags=["Consent CDC"])
async def consent_cdc_audit():
    # Dummy audit logic
    return {"status": "success"}

@consent_cdc_router.post("/bulk-download-changes", tags=["Consent CDC"])
async def bulk_download_changes():
    cdc_records = await db["consent_cdc"].find().to_list(100)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=cdc_records[0].keys())
    writer.writeheader()
    for record in cdc_records:
        writer.writerow(record)
    output.seek(0)
    return {"data": output.getvalue()}

@consent_cdc_router.post("/subscribe-collection-point", tags=["Consent CDC"])
async def subscribe_collection_point(collection_point_id: str):
    # Logic to subscribe to collection point changes
    return {"status": "subscribed", "collection_point_id": collection_point_id}

@consent_cdc_router.post("/subscribe-app", tags=["Consent CDC"])
async def subscribe_app(app_id: str):
    # Logic to subscribe to app changes
    return {"status": "subscribed", "app_id": app_id}

@consent_cdc_router.post("/subscribe-data-principal", tags=["Consent CDC"])
async def subscribe_data_principal(data_principal_id: str):
    # Logic to subscribe to data principal changes
    return {"status": "subscribed", "data_principal_id": data_principal_id}
