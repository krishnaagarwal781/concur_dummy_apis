from fastapi import APIRouter, HTTPException, UploadFile, File
from models.models import BreachTemplate, BreachIncident, BreachNotificationArtifact, BreachNotification, DataBreachInvestigation
from config.database import db
from bson import ObjectId
from typing import List
from datetime import datetime

data_breach_router = APIRouter()

@data_breach_router.get("/get-breach-template/{template_id}", tags=["Data Breach Management"])
async def get_breach_template(template_id: str):
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    template = await db["breach_templates"].find_one({"_id": ObjectId(template_id)})
    if template:
        return template
    raise HTTPException(status_code=404, detail="Breach template not found")

@data_breach_router.post("/create-breach-incident", tags=["Data Breach Management"])
async def create_breach_incident(incident: BreachIncident):
    result = await db["breach_incidents"].insert_one(incident.dict())
    return {"incident_id": str(result.inserted_id)}

@data_breach_router.put("/update-breach-incident/{incident_id}", tags=["Data Breach Management"])
async def update_breach_incident(incident_id: str, incident: BreachIncident):
    if not ObjectId.is_valid(incident_id):
        raise HTTPException(status_code=400, detail="Invalid incident ID")
    result = await db["breach_incidents"].update_one({"_id": ObjectId(incident_id)}, {"$set": incident.dict(exclude_unset=True)})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Breach incident not found")

@data_breach_router.post("/data-breach-investigation", tags=["Data Breach Management"])
async def data_breach_investigation(investigation: DataBreachInvestigation):
    result = await db["data_breach_investigations"].insert_one(investigation.dict())
    return {"investigation_id": str(result.inserted_id)}

@data_breach_router.get("/list-data-breach-incidents", tags=["Data Breach Management"])
async def list_data_breach_incidents():
    incidents = await db["breach_incidents"].find().to_list(100)
    return incidents

@data_breach_router.post("/create-breach-notification-artifact", tags=["Data Breach Management"])
async def create_breach_notification_artifact(artifact: BreachNotificationArtifact):
    result = await db["breach_notification_artifacts"].insert_one(artifact.dict())
    return {"artifact_id": str(result.inserted_id)}

@data_breach_router.put("/publish-breach-notification-artifact/{artifact_id}", tags=["Data Breach Management"])
async def publish_breach_notification_artifact(artifact_id: str):
    if not ObjectId.is_valid(artifact_id):
        raise HTTPException(status_code=400, detail="Invalid artifact ID")
    result = await db["breach_notification_artifacts"].update_one({"_id": ObjectId(artifact_id)}, {"$set": {"published_at": datetime.utcnow()}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Notification artifact not found")

@data_breach_router.post("/data-breach-notification", tags=["Data Breach Management"])
async def data_breach_notification(notification: BreachNotification):
    result = await db["breach_notifications"].insert_one(notification.dict())
    # Here, you might want to send the notification to the recipients
    return {"notification_id": str(result.inserted_id)}
