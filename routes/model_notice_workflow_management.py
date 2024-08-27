from fastapi import APIRouter, HTTPException
from models.models import ModelNoticeWorkflow, UpdateModelNoticeWorkflow, ModelNoticeWorkflowInsights, AuditModelNoticeWorkflow
from config.database import db
from bson import ObjectId

workflow_router = APIRouter()

@workflow_router.post("/create-model-notice-workflow", tags=["Model Notice Workflow Management"])
async def create_model_notice_workflow(workflow: ModelNoticeWorkflow):
    result = await db["model_notice_workflows"].insert_one(workflow.dict())
    return {"id": str(result.inserted_id)}

@workflow_router.get("/get-model-notice-workflow/{workflow_id}", tags=["Model Notice Workflow Management"])
async def get_model_notice_workflow(workflow_id: str):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    workflow = await db["model_notice_workflows"].find_one({"_id": ObjectId(workflow_id)})
    if workflow:
        return workflow
    raise HTTPException(status_code=404, detail="Model notice workflow not found")

@workflow_router.get("/view-model-notice-workflow/{workflow_id}", tags=["Model Notice Workflow Management"])
async def view_model_notice_workflow(workflow_id: str):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    workflow = await db["model_notice_workflows"].find_one({"_id": ObjectId(workflow_id)})
    if workflow:
        return workflow
    raise HTTPException(status_code=404, detail="Model notice workflow not found")

@workflow_router.put("/update-model-notice-workflow/{workflow_id}", tags=["Model Notice Workflow Management"])
async def update_model_notice_workflow(workflow_id: str, workflow: UpdateModelNoticeWorkflow):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    result = await db["model_notice_workflows"].update_one({"_id": ObjectId(workflow_id)}, {"$set": workflow.dict(exclude_unset=True)})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice workflow not found")

@workflow_router.put("/publish-model-notice-workflow/{workflow_id}", tags=["Model Notice Workflow Management"])
async def publish_model_notice_workflow(workflow_id: str):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    result = await db["model_notice_workflows"].update_one({"_id": ObjectId(workflow_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice workflow not found")

@workflow_router.get("/list-model-notice-workflows", tags=["Model Notice Workflow Management"])
async def list_model_notice_workflows():
    workflows = await db["model_notice_workflows"].find().to_list(100)
    return workflows

@workflow_router.delete("/delete-model-notice-workflow/{workflow_id}", tags=["Model Notice Workflow Management"])
async def delete_model_notice_workflow(workflow_id: str):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    result = await db["model_notice_workflows"].delete_one({"_id": ObjectId(workflow_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Model notice workflow not found")

@workflow_router.post("/audit-model-notice-workflow/{workflow_id}", tags=["Model Notice Workflow Management"])
async def audit_model_notice_workflow(workflow_id: str, audit_data: AuditModelNoticeWorkflow):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    # Dummy audit logic
    return {"status": "success", "analysis": audit_data.analysis}

@workflow_router.get("/model-notice-workflow-insights/{workflow_id}", tags=["Model Notice Workflow Management"])
async def model_notice_workflow_insights(workflow_id: str):
    if not ObjectId.is_valid(workflow_id):
        raise HTTPException(status_code=400, detail="Invalid workflow ID")
    # Dummy insights response
    return {"workflow_id": workflow_id, "insights": {"usage": 100, "performance": 75}}
