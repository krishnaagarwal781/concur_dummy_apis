from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
from models.models import Credentials, UpdateCredentials
from config.database import db
from bson import ObjectId
import base64
import json
import io

credential_router = APIRouter()


@credential_router.post("/create-credentials", tags=["Credentials Management"])
async def create_credentials(credentials: Credentials):
    encrypted_password = cipher_suite.encrypt(credentials.password.encode()).decode()
    credentials_dict = credentials.dict()
    credentials_dict["password"] = encrypted_password
    result = await db["credentials"].insert_one(credentials_dict)
    return {"id": str(result.inserted_id)}

@credential_router.put("/update-credentials/{credentials_id}", tags=["Credentials Management"])
async def update_credentials(credentials_id: str, credentials: UpdateCredentials):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    
    update_dict = credentials.dict(exclude_unset=True)
    if "password" in update_dict:
        update_dict["password"] = cipher_suite.encrypt(update_dict["password"].encode()).decode()
    
    result = await db["credentials"].update_one({"_id": ObjectId(credentials_id)}, {"$set": update_dict})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Credentials not found")

@credential_router.post("/attach-credentials/{credentials_id}", tags=["Credentials Management"])
async def attach_credentials(credentials_id: str, service: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    
    result = await db["credentials"].update_one({"_id": ObjectId(credentials_id)}, {"$set": {"service": service}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Credentials not found")

@credential_router.post("/remove-credentials/{credentials_id}", tags=["Credentials Management"])
async def remove_credentials(credentials_id: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    
    result = await db["credentials"].update_one({"_id": ObjectId(credentials_id)}, {"$set": {"status": "inactive"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Credentials not found")

@credential_router.delete("/delete-credentials/{credentials_id}", tags=["Credentials Management"])
async def delete_credentials(credentials_id: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    
    result = await db["credentials"].delete_one({"_id": ObjectId(credentials_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Credentials not found")

@credential_router.get("/get-credentials/{credentials_id}", tags=["Credentials Management"])
async def get_credentials(credentials_id: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    
    credentials = await db["credentials"].find_one({"_id": ObjectId(credentials_id)})
    if credentials:
        credentials["password"] = cipher_suite.decrypt(credentials["password"].encode()).decode()
        return credentials
    raise HTTPException(status_code=404, detail="Credentials not found")

@credential_router.get("/list-credentials", tags=["Credentials Management"])
async def list_credentials():
    credentials_list = await db["credentials"].find().to_list(100)
    for cred in credentials_list:
        cred["password"] = cipher_suite.decrypt(cred["password"].encode()).decode()
    return credentials_list

@credential_router.post("/validate-credentials/{credentials_id}", tags=["Credentials Management"])
async def validate_credentials(credentials_id: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    # Dummy validation response
    return {"credentials_id": credentials_id, "status": "valid"}

@credential_router.post("/encrypt-credentials", tags=["Credentials Management"])
async def encrypt_credentials(credentials: Credentials):
    encrypted_password = cipher_suite.encrypt(credentials.password.encode()).decode()
    return {"encrypted_password": encrypted_password}

@credential_router.post("/rotate-credentials/{credentials_id}", tags=["Credentials Management"])
async def rotate_credentials(credentials_id: str, new_password: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(status_code=400, detail="Invalid credentials ID")
    
    encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()
    result = await db["credentials"].update_one({"_id": ObjectId(credentials_id)}, {"$set": {"password": encrypted_password}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Credentials not found")
