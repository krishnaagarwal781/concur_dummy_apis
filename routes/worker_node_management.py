from fastapi import APIRouter, HTTPException
from typing import List
from models.models import WorkerNode, UpdateWorkerNode
from config.database import db
from bson import ObjectId

worker_router = APIRouter()

@worker_router.get("/worker-node-dashboard", tags=["Worker Node Management"])
async def worker_node_dashboard():
    # Dashboard response with a summary of worker nodes (e.g., total active nodes, etc.)
    total_nodes = await db["worker_nodes"].count_documents({})
    active_nodes = await db["worker_nodes"].count_documents({"status": "active"})
    return {"total_nodes": total_nodes, "active_nodes": active_nodes}

@worker_router.get("/get-worker-node-template", tags=["Worker Node Management"])
async def get_worker_node_template():
    # Returns a template for creating a new worker node
    return WorkerNode.schema()

@worker_router.post("/create-worker-node", tags=["Worker Node Management"])
async def create_worker_node(worker_node: WorkerNode):
    result = await db["worker_nodes"].insert_one(worker_node.dict())
    return {"id": str(result.inserted_id)}

@worker_router.get("/view-worker-node/{node_id}", tags=["Worker Node Management"])
async def view_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    node = await db["worker_nodes"].find_one({"_id": ObjectId(node_id)})
    if node:
        return node
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.get("/worker-node-stats/{node_id}", tags=["Worker Node Management"])
async def worker_node_stats(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    node = await db["worker_nodes"].find_one({"_id": ObjectId(node_id)})
    if node:
        return {"node_id": node_id, "stats": node.get("stats", {})}
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.put("/update-worker-node/{node_id}", tags=["Worker Node Management"])
async def update_worker_node(node_id: str, worker_node: UpdateWorkerNode):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    update_dict = worker_node.dict(exclude_unset=True)
    result = await db["worker_nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": update_dict})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.put("/publish-worker-node/{node_id}", tags=["Worker Node Management"])
async def publish_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    result = await db["worker_nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.delete("/delete-worker-node/{node_id}", tags=["Worker Node Management"])
async def delete_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    result = await db["worker_nodes"].delete_one({"_id": ObjectId(node_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.get("/list-worker-nodes", tags=["Worker Node Management"])
async def list_worker_nodes():
    nodes = await db["worker_nodes"].find().to_list(100)
    return nodes

@worker_router.post("/activate-worker-node/{node_id}", tags=["Worker Node Management"])
async def activate_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    result = await db["worker_nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": {"status": "active"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.post("/deactivate-worker-node/{node_id}", tags=["Worker Node Management"])
async def deactivate_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    result = await db["worker_nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": {"status": "inactive"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Worker node not found")

@worker_router.post("/restart-worker-node/{node_id}", tags=["Worker Node Management"])
async def restart_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    # Dummy restart response
    return {"status": "Worker node restarted", "node_id": node_id}

@worker_router.post("/scale-worker-nodes", tags=["Worker Node Management"])
async def scale_worker_nodes(scale: int):
    # Dummy scale response
    return {"status": "Worker nodes scaled", "scale_to": scale}

@worker_router.get("/monitor-worker-node/{node_id}", tags=["Worker Node Management"])
async def monitor_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    # Dummy monitor response
    return {"node_id": node_id, "status": "healthy", "metrics": {}}

@worker_router.post("/sync-worker-node/{node_id}", tags=["Worker Node Management"])
async def sync_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    # Dummy sync response
    return {"status": "Worker node synchronized", "node_id": node_id}

@worker_router.post("/rollback-worker-node/{node_id}", tags=["Worker Node Management"])
async def rollback_worker_node(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    # Dummy rollback response
    return {"status": "Worker node rolled back", "node_id": node_id}

@worker_router.get("/worker-node-logs/{node_id}", tags=["Worker Node Management"])
async def worker_node_logs(node_id: str):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=400, detail="Invalid node ID")
    # Dummy logs response
    return {"node_id": node_id, "logs": []}
