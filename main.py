from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    app_management,
    campaign_management,
    collection_point_management,
    consent_cdc,
    consent_management,
    credentials_management,
    data_breach_management,
    data_catalogue_management,
    data_classification,
    data_element_management,
    data_principal,
    data_principal_persona,
    data_source_management,
    dpar,
    dpo,
    model_notice_workflow_management,
    model_notice,
    preference_center,
    progressive_consent,
    reconsent_management,
    scan_profile_management,
    worker_node_management,
)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to backend"}


app.include_router(app_management.app_management_router)
app.include_router(campaign_management.campaign_router)
app.include_router(collection_point_management.collection_router)
app.include_router(consent_cdc.consent_cdc_router)
app.include_router(consent_management.consent_router)
app.include_router(credentials_management.credential_router)
app.include_router(data_breach_management.data_breach_router)
app.include_router(data_catalogue_management.catalogue_router)
app.include_router(data_classification.data_classification_router)
app.include_router(data_element_management.element_router)
app.include_router(data_principal.data_principal_router)
app.include_router(data_principal_persona.data_principal_persona_router)
app.include_router(data_source_management.data_source_router)
app.include_router(dpar.dpar_router)
app.include_router(dpo.dpo_router)
app.include_router(model_notice_workflow_management.workflow_router)
app.include_router(model_notice.modelNotice)
app.include_router(preference_center.preference_centre_router)
app.include_router(progressive_consent.progressive_consent_router)
app.include_router(reconsent_management.reconsent_router)
app.include_router(scan_profile_management.profile_router)
app.include_router(worker_node_management.worker_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
