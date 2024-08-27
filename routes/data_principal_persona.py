from fastapi import APIRouter, HTTPException
from models.models import Persona, UpdatePersona
from config.database import db
from bson import ObjectId

data_principal_persona_router = APIRouter()

@data_principal_persona_router.get("/get-all-persona", tags=["Data Principal Persona"])
async def get_all_persona():
    personas = await db["personas"].find().to_list(100)
    return personas

@data_principal_persona_router.post("/create-persona", tags=["Data Principal Persona"])
async def create_persona(persona: Persona):
    result = await db["personas"].insert_one(persona.dict())
    return {"id": str(result.inserted_id)}

@data_principal_persona_router.get("/get-persona/{persona_id}", tags=["Data Principal Persona"])
async def get_persona(persona_id: str):
    if not ObjectId.is_valid(persona_id):
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    persona = await db["personas"].find_one({"_id": ObjectId(persona_id)})
    if persona:
        return persona
    raise HTTPException(status_code=404, detail="Persona not found")

@data_principal_persona_router.put("/update-persona/{persona_id}", tags=["Data Principal Persona"])
async def update_persona(persona_id: str, persona: UpdatePersona):
    if not ObjectId.is_valid(persona_id):
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    result = await db["personas"].update_one(
        {"_id": ObjectId(persona_id)}, {"$set": persona.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Persona not found")

@data_principal_persona_router.put("/publish-persona/{persona_id}", tags=["Data Principal Persona"])
async def publish_persona(persona_id: str):
    if not ObjectId.is_valid(persona_id):
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    result = await db["personas"].update_one(
        {"_id": ObjectId(persona_id)}, {"$set": {"status": "published"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Persona not found")

@data_principal_persona_router.put("/unpublish-persona/{persona_id}", tags=["Data Principal Persona"])
async def unpublish_persona(persona_id: str):
    if not ObjectId.is_valid(persona_id):
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    result = await db["personas"].update_one(
        {"_id": ObjectId(persona_id)}, {"$set": {"status": "unpublished"}}
    )
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Persona not found")

@data_principal_persona_router.get("/persona-insights/{persona_id}", tags=["Data Principal Persona"])
async def persona_insights(persona_id: str):
    if not ObjectId.is_valid(persona_id):
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    # Dummy insights response
    return {
        "persona_id": persona_id,
        "insights": {"total_consents": 50, "active_consents": 45},
    }
