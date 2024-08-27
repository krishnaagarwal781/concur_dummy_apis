from fastapi import APIRouter, HTTPException, UploadFile, File
from models.models import (
    DataPrincipal,
    DPARRequest,
    DPARStatusDashboard,
    DPDataExport,
    VerifyEmailResponse,
    VerifyMobileResponse,
    VerifyKYCResponse,
    ReKYCRequest,
)
from config.database import db
from bson import ObjectId
from datetime import datetime
from typing import List, Dict

dpar_router = APIRouter()


@dpar_router.post("/login", tags=["Data Principal Access Request"])
async def login(email: str, password: str):
    # Logic to authenticate user
    return {"status": "logged in"}


@dpar_router.post("/verify-email", tags=["Data Principal Access Request"])
async def verify_email(email: str) -> VerifyEmailResponse:
    # Logic to verify email
    return {"verified": True, "message": "Email verified successfully"}


@dpar_router.post("/verify-mobile", tags=["Data Principal Access Request"])
async def verify_mobile(phone: str) -> VerifyMobileResponse:
    # Logic to verify mobile
    return {"verified": True, "message": "Mobile number verified successfully"}


@dpar_router.post("/verify-kyc", tags=["Data Principal Access Request"])
async def verify_kyc(user_id: str) -> VerifyKYCResponse:
    # Logic to verify KYC
    return {"verified": True, "message": "KYC verified successfully"}


@dpar_router.post("/rekyc-request", tags=["Data Principal Access Request"])
async def rekyc_request(request: ReKYCRequest):
    # Logic to handle re-KYC request
    return {"status": "Re-KYC request submitted"}


@dpar_router.get("/get-dp-profile/{user_id}", tags=["Data Principal Access Request"])
async def get_dp_profile(user_id: str):
    profile = await db["data_principals"].find_one({"_id": ObjectId(user_id)})
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Data Principal profile not found")


@dpar_router.get("/list-dpar-requests", tags=["Data Principal Access Request"])
async def list_dpar_requests():
    requests = await db["dpar_requests"].find().to_list(100)
    return requests


@dpar_router.post("/create-dpar-request", tags=["Data Principal Access Request"])
async def create_dpar_request(request: DPARRequest):
    result = await db["dpar_requests"].insert_one(request.dict())
    return {"request_id": str(result.inserted_id)}


@dpar_router.post(
    "/cancel-dpar-request/{request_id}", tags=["Data Principal Access Request"]
)
async def cancel_dpar_request(request_id: str):
    result = await db["dpar_requests"].update_one(
        {"request_id": request_id}, {"$set": {"status": "cancelled"}}
    )
    if result.matched_count:
        return {"status": "request cancelled"}
    raise HTTPException(status_code=404, detail="Request not found")


@dpar_router.get("/dpar-status-dashboard", tags=["Data Principal Access Request"])
async def dpar_status_dashboard() -> DPARStatusDashboard:
    total_requests = await db["dpar_requests"].count_documents({})
    pending_requests = await db["dpar_requests"].count_documents({"status": "pending"})
    approved_requests = await db["dpar_requests"].count_documents(
        {"status": "approved"}
    )
    rejected_requests = await db["dpar_requests"].count_documents(
        {"status": "rejected"}
    )

    return {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "rejected_requests": rejected_requests,
    }


@dpar_router.get(
    "/dpar-request-status/{request_id}", tags=["Data Principal Access Request"]
)
async def dpar_request_status(request_id: str):
    request = await db["dpar_requests"].find_one({"request_id": request_id})
    if request:
        return request
    raise HTTPException(status_code=404, detail="Request not found")


@dpar_router.get("/download-dp-data/{user_id}", tags=["Data Principal Access Request"])
async def download_dp_data(user_id: str) -> DPDataExport:
    data = await db["data_principals"].find_one({"_id": ObjectId(user_id)})
    if data:
        return DPDataExport(user_id=user_id, data=data)
    raise HTTPException(status_code=404, detail="Data not found")


@dpar_router.post("/enable-nomination", tags=["Data Principal Access Request"])
async def enable_nomination(user_id: str):
    # Logic to enable nomination
    return {"status": "nomination enabled"}


@dpar_router.put(
    "/update-dpar-request/{request_id}", tags=["Data Principal Access Request"]
)
async def update_dpar_request(request_id: str, request: DPARRequest):
    result = await db["dpar_requests"].update_one(
        {"request_id": request_id}, {"$set": request.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "request updated"}
    raise HTTPException(status_code=404, detail="Request not found")


@dpar_router.post("/validate-dpar-request", tags=["Data Principal Access Request"])
async def validate_dpar_request(request: DPARRequest):
    # Logic to validate the request
    return {"status": "request validated"}


@dpar_router.post("/upload-dp-documents", tags=["Data Principal Access Request"])
async def upload_dp_documents(user_id: str, files: List[UploadFile] = File(...)):
    # Logic to handle document uploads
    return {"status": "documents uploaded"}


@dpar_router.post("/notify-dpar-status", tags=["Data Principal Access Request"])
async def notify_dpar_status(user_id: str, status: str):
    # Logic to send notifications
    return {"status": "notification sent"}
