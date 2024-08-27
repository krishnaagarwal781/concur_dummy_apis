from fastapi import APIRouter, HTTPException
from typing import List
from models.models import (
    ClassificationTemplate, CountryTemplate, CustomClassifier, 
    UpdateCustomClassifier, ClassificationAssignment, ClassificationAudit
)
from config.database import db
from bson import ObjectId

data_classification_router = APIRouter()

@data_classification_router.get("/get-classification-template", tags=["Data Classification"])
async def get_classification_template():
    templates = await db["classification_templates"].find().to_list(100)
    return templates

@data_classification_router.get("/get-country-template", tags=["Data Classification"])
async def get_country_template():
    countries = await db["country_templates"].find().to_list(100)
    return countries

@data_classification_router.post("/create-custom-classifier", tags=["Data Classification"])
async def create_custom_classifier(classifier: CustomClassifier):
    result = await db["custom_classifiers"].insert_one(classifier.dict())
    return {"id": str(result.inserted_id)}

@data_classification_router.get("/view-custom-classifier/{classifier_id}", tags=["Data Classification"])
async def view_custom_classifier(classifier_id: str):
    if not ObjectId.is_valid(classifier_id):
        raise HTTPException(status_code=400, detail="Invalid classifier ID")
    classifier = await db["custom_classifiers"].find_one({"_id": ObjectId(classifier_id)})
    if classifier:
        return classifier
    raise HTTPException(status_code=404, detail="Custom classifier not found")

@data_classification_router.put("/update-custom-classifier/{classifier_id}", tags=["Data Classification"])
async def update_custom_classifier(classifier_id: str, classifier: UpdateCustomClassifier):
    if not ObjectId.is_valid(classifier_id):
        raise HTTPException(status_code=400, detail="Invalid classifier ID")
    update_dict = classifier.dict(exclude_unset=True)
    result = await db["custom_classifiers"].update_one({"_id": ObjectId(classifier_id)}, {"$set": update_dict})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Custom classifier not found")

@data_classification_router.put("/publish-custom-classifier/{classifier_id}", tags=["Data Classification"])
async def publish_custom_classifier(classifier_id: str):
    if not ObjectId.is_valid(classifier_id):
        raise HTTPException(status_code=400, detail="Invalid classifier ID")
    result = await db["custom_classifiers"].update_one({"_id": ObjectId(classifier_id)}, {"$set": {"status": "published"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Custom classifier not found")

@data_classification_router.put("/unpublish-custom-classifier/{classifier_id}", tags=["Data Classification"])
async def unpublish_custom_classifier(classifier_id: str):
    if not ObjectId.is_valid(classifier_id):
        raise HTTPException(status_code=400, detail="Invalid classifier ID")
    result = await db["custom_classifiers"].update_one({"_id": ObjectId(classifier_id)}, {"$set": {"status": "unpublished"}})
    if result.matched_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Custom classifier not found")

@data_classification_router.delete("/delete-custom-classifier/{classifier_id}", tags=["Data Classification"])
async def delete_custom_classifier(classifier_id: str):
    if not ObjectId.is_valid(classifier_id):
        raise HTTPException(status_code=400, detail="Invalid classifier ID")
    result = await db["custom_classifiers"].delete_one({"_id": ObjectId(classifier_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Custom classifier not found")

@data_classification_router.post("/assign-classification", tags=["Data Classification"])
async def assign_classification(assignment: ClassificationAssignment):
    # Dummy assignment logic
    return {"status": "success", "assignment": assignment}

@data_classification_router.post("/classify-data-element", tags=["Data Classification"])
async def classify_data_element(data_element_id: str, classification_id: str):
    # Dummy classification logic
    return {"status": "success", "data_element_id": data_element_id, "classification_id": classification_id}

@data_classification_router.post("/audit-classification", tags=["Data Classification"])
async def audit_classification(audit: ClassificationAudit):
    # Dummy audit logic
    return {"status": "success", "audit": audit}

@data_classification_router.put("/reclassify-data", tags=["Data Classification"])
async def reclassify_data(data_element_id: str, new_classification_id: str):
    # Dummy reclassification logic
    return {"status": "success", "data_element_id": data_element_id, "new_classification_id": new_classification_id}

@data_classification_router.get("/list-classifications", tags=["Data Classification"])
async def list_classifications():
    classifications = await db["data_classifications"].find().to_list(100)
    return classifications

@data_classification_router.get("/validate-classification/{classification_id}", tags=["Data Classification"])
async def validate_classification(classification_id: str):
    if not ObjectId.is_valid(classification_id):
        raise HTTPException(status_code=400, detail="Invalid classification ID")
    # Dummy validation logic
    return {"status": "valid", "classification_id": classification_id}
