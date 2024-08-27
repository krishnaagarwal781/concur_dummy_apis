from fastapi import APIRouter, HTTPException
from typing import List
from models.models import App, UpdateApp, AppAnalytics, ConsentInsights, ExportAppData, ImportAppData, AuditApp, ConsentHistory
from config.database import db
from bson import ObjectId

app_management_router = APIRouter()

@app_management_router.post("/register-app", tags=["App Management"])
async def register_app(app: App):
    result = await db["apps"].insert_one(app.dict())
    return {"id": str(result.inserted_id)}

@app_management_router.get("/get-app-list", tags=["App Management"])
async def get_app_list():
    apps = await db["apps"].find().to_list(100)
    return apps

@app_management_router.put("/update-app/{app_id}", tags=["App Management"])
async def update_app(app_id: str, app: UpdateApp):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": app.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")

@app_management_router.put("/publish-app/{app_id}", tags=["App Management"])
async def publish_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")

@app_management_router.put("/unpublish-app/{app_id}", tags=["App Management"])
async def unpublish_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")

@app_management_router.post("/activate-app/{app_id}", tags=["App Management"])
async def activate_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"status": "active"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")

@app_management_router.post("/deactivate-app/{app_id}", tags=["App Management"])
async def deactivate_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"status": "inactive"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")

@app_management_router.get("/app-analytics/{app_id}", tags=["App Management"])
async def app_analytics(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    # Dummy analytics response
    return {"app_id": app_id, "usage_metrics": {}, "performance_metrics": {}, "user_interactions": {}}

@app_management_router.get("/consent-insights/{app_id}", tags=["App Management"])
async def consent_insights(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    # Dummy insights response
    return {"app_id": app_id, "consent_interactions": {}}

@app_management_router.post("/export-app-data", tags=["App Management"])
async def export_app_data(export_data: ExportAppData):
    # Dummy export logic
    return {"status": "success", "format": export_data.format}

@app_management_router.post("/import-app-data", tags=["App Management"])
async def import_app_data(import_data: ImportAppData):
    # Dummy import logic
    return {"status": "success", "format": import_data.format}

@app_management_router.post("/audit-app", tags=["App Management"])
async def audit_app(audit: AuditApp):
    # Dummy audit logic
    return {"status": "success", "audit_result": audit.audit_result, "compliance_status": audit.compliance_status}

@app_management_router.get("/get-consent-history/{app_id}", tags=["App Management"])
async def get_consent_history(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    # Dummy consent history response
    return {"app_id": app_id, "consent_actions": []}

@app_management_router.post("/sync-app/{app_id}", tags=["App Management"])
async def sync_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    # Dummy sync logic
    return {"status": "success"}

@app_management_router.post("/assign-consent-policy/{app_id}", tags=["App Management"])
async def assign_consent_policy(app_id: str, consent_policy: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    result = await db["apps"].update_one(
        {"_id": ObjectId(app_id)}, {"$set": {"consent_policy": consent_policy}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="App not found")

@app_management_router.get("/validate-app/{app_id}", tags=["App Management"])
async def validate_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid app ID")
    # Dummy validation logic
    return {"status": "valid", "app_id": app_id}
