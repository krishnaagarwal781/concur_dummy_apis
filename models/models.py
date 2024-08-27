from pydantic import BaseModel
from typing import Optional, List, Dict
from bson import ObjectId
from datetime import datetime


class App(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "inactive"  # e.g., "active", "inactive", "published", "unpublished"
    consent_policy: Optional[str] = None


class UpdateApp(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]  # e.g., "active", "inactive", "published", "unpublished"
    consent_policy: Optional[str]


class AppAnalytics(BaseModel):
    app_id: str
    usage_metrics: dict  # Metrics related to app usage
    performance_metrics: dict  # Metrics related to app performance
    user_interactions: dict  # Metrics related to user interactions


class ConsentInsights(BaseModel):
    app_id: str
    consent_interactions: dict  # Insights related to user consent


class ExportAppData(BaseModel):
    app_id: str
    format: str  # e.g., "json", "csv"


class ImportAppData(BaseModel):
    format: str  # e.g., "json", "csv"
    data: dict  # Data to import


class AuditApp(BaseModel):
    app_id: str
    audit_result: str
    compliance_status: str


class ConsentHistory(BaseModel):
    app_id: str
    consent_actions: List[dict]  # List of consent actions


# Collection point management models
class CollectionPoint(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "inactive"  # e.g., "active", "inactive", "published", "unpublished"
    data_format: Optional[str] = None


class UpdateCollectionPoint(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]  # e.g., "active", "inactive", "published", "unpublished"
    data_format: Optional[str]


class CollectionPointInsights(BaseModel):
    point_id: str
    metrics: Dict[str, int]  # Metrics related to performance and usage


class ExportCollectionPointData(BaseModel):
    point_id: str
    format: str  # e.g., "json", "csv"


class ImportCollectionPointData(BaseModel):
    format: str  # e.g., "json", "csv"
    data: dict  # Data to import


class AuditCollectionPoint(BaseModel):
    point_id: str
    audit_result: str
    compliance_status: str


# Persona management models
class Persona(BaseModel):
    name: str
    description: Optional[str]
    status: str = "draft"  # draft, published, unpublished


class UpdatePersona(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]


# Data principal management models
class DataPrincipal(BaseModel):
    name: str
    email: str


class UpdateDataPrincipal(BaseModel):
    name: Optional[str]
    email: Optional[str]


# Model notice management models
class ModelNotice(BaseModel):
    title: str
    content: str
    status: str = "draft"  # e.g., "draft", "published", "unpublished"
    language: Optional[str] = None


class UpdateModelNotice(BaseModel):
    title: Optional[str]
    content: Optional[str]
    status: Optional[str]  # e.g., "draft", "published", "unpublished"
    language: Optional[str]


class ModelNoticeInsights(BaseModel):
    template_id: str
    metrics: Dict[str, int]  # Insights related to usage and effectiveness


class ExportModelNotice(BaseModel):
    template_id: str
    format: str  # e.g., "pdf", "json"


class ImportModelNotice(BaseModel):
    format: str  # e.g., "pdf", "json"
    data: dict  # Data to import


class SearchModelNotice(BaseModel):
    query: str
    filters: Optional[Dict[str, str]]  # Filters for search criteria


class DataSource(BaseModel):
    name: str
    datasource_type: str
    configuration: dict
    status: str = "active"  # e.g., active, archived, inactive


class UpdateDataSource(BaseModel):
    name: Optional[str]
    datasource_type: Optional[str]
    configuration: Optional[dict]
    status: Optional[str]


class Credentials(BaseModel):
    username: str
    password: str
    service: str  # Service or application for which the credentials are used
    status: str = "active"  # e.g., active, inactive, archived


class UpdateCredentials(BaseModel):
    username: Optional[str]
    password: Optional[str]
    service: Optional[str]
    status: Optional[str]


class WorkerNode(BaseModel):
    name: str
    ip_address: str
    status: str = "inactive"  # e.g., active, inactive, published, etc.
    configuration: Optional[dict] = {}  # Configuration details for the worker node
    stats: Optional[dict] = {}  # Metrics or statistics related to the worker node


class UpdateWorkerNode(BaseModel):
    name: Optional[str]
    ip_address: Optional[str]
    status: Optional[str]
    configuration: Optional[dict]
    stats: Optional[dict]


class DataCatalogue(BaseModel):
    name: str
    description: Optional[str] = None
    entries: List[dict]  # List of entries in the data catalogue
    status: str = "inactive"  # e.g., active, inactive, published, unpublished
    categories: Optional[List[str]] = None  # Optional categories or classifications


class UpdateDataCatalogue(BaseModel):
    name: Optional[str]
    description: Optional[str]
    entries: Optional[List[dict]]
    status: Optional[str]
    categories: Optional[List[str]]


class DataElement(BaseModel):
    name: str
    description: Optional[str] = None
    element_type: str
    status: str = "inactive"
    categories: Optional[List[str]] = None


class UpdateDataElement(BaseModel):
    name: Optional[str]
    description: Optional[str]
    element_type: Optional[str]
    status: Optional[str]
    categories: Optional[List[str]]


class ClassificationTemplate(BaseModel):
    name: str
    description: Optional[str] = None
    criteria: dict  # Define the criteria for this classification template


class CountryTemplate(BaseModel):
    country_code: str
    country_name: str


class CustomClassifier(BaseModel):
    name: str
    description: Optional[str] = None
    rules: dict  # Define the rules for this custom classifier


class UpdateCustomClassifier(BaseModel):
    name: Optional[str]
    description: Optional[str]
    rules: Optional[dict]


class ClassificationAssignment(BaseModel):
    element_id: str
    classification_id: str


class ClassificationAudit(BaseModel):
    element_id: str
    classification_id: str
    audit_date: str
    audit_result: str


class ModelNoticeWorkflow(BaseModel):
    name: str
    description: Optional[str] = None
    steps: Dict[str, str]  # Steps and their descriptions in the workflow
    status: str = "draft"  # e.g., "draft", "published"


class UpdateModelNoticeWorkflow(BaseModel):
    name: Optional[str]
    description: Optional[str]
    steps: Optional[Dict[str, str]]
    status: Optional[str]  # e.g., "draft", "published"


class ModelNoticeWorkflowInsights(BaseModel):
    workflow_id: str
    metrics: Dict[str, int]  # Insights related to usage and performance


class AuditModelNoticeWorkflow(BaseModel):
    workflow_id: str
    analysis: Dict[str, str]  # Analysis details, such as cost evaluation


class Campaign(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "draft"  # e.g., "draft", "published"
    schedule_time: Optional[datetime] = None  # Time to schedule the campaign


class UpdateCampaign(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]  # e.g., "draft", "published"
    schedule_time: Optional[datetime]


class CampaignAnalytics(BaseModel):
    campaign_id: str
    metrics: Dict[str, int]  # Metrics related to campaign performance


class CampaignInsights(BaseModel):
    campaign_id: str
    insights: Dict[str, str]  # Detailed insights and metrics


class ExportCampaignData(BaseModel):
    campaign_id: str
    format: str  # e.g., "CSV", "JSON"


class ImportCampaignData(BaseModel):
    data: Dict  # The data to import


class Consent(BaseModel):
    user_id: str
    consent_type: str
    status: str  # e.g., "granted", "revoked"
    timestamp: datetime
    details: Optional[Dict] = None


class ConsentArtifact(BaseModel):
    consent_id: str
    artifact_data: Dict


class ConsentHistory(BaseModel):
    user_id: str
    history: List[Dict]  # List of consent records or changes


class ConsentInsights(BaseModel):
    user_id: str
    insights: Dict  # Detailed insights on consent history


class BulkUploadConsents(BaseModel):
    consents: List[Consent]


class ConsentReport(BaseModel):
    user_id: str
    report_data: Dict  # Detailed consent report data


class ConsentCDC(BaseModel):
    consent_id: str
    change_type: str  # e.g., "created", "updated", "deleted"
    change_timestamp: datetime
    details: Dict


class ConsentCDCInsights(BaseModel):
    total_changes: int
    changes_by_type: Dict[str, int]  # e.g., {"created": 10, "updated": 5, "deleted": 2}


class ConsentCDCAudit(BaseModel):
    audit_data: Dict  # Details of the audit findings


class ReconsentRule(BaseModel):
    rule_id: str
    description: str
    criteria: Dict  # Criteria for triggering reconsent
    created_at: datetime
    updated_at: datetime


class ReconsentDetails(BaseModel):
    rule_id: str
    status: str  # e.g., "pending", "completed", "failed"
    request_timestamp: datetime
    response_timestamp: datetime


class ReconsentInsights(BaseModel):
    total_requests: int
    total_responses: int
    compliance_rate: float


class ReconsentAudit(BaseModel):
    audit_data: Dict


class ProgressiveConsentRule(BaseModel):
    rule_id: str
    description: str
    criteria: Dict  # Criteria for triggering progressive consent
    created_at: datetime
    updated_at: datetime


class ProgressiveConsentDetails(BaseModel):
    rule_id: str
    status: str  # e.g., "pending", "accepted", "rejected"
    request_timestamp: datetime
    response_timestamp: datetime


class ProgressiveConsentInsights(BaseModel):
    total_requests: int
    total_acceptances: int
    total_rejections: int
    acceptance_rate: float


class ProgressiveConsentAudit(BaseModel):
    audit_data: Dict  # Details of the audit findings


class DataPrincipal(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]


class UserPreference(BaseModel):
    user_id: str
    preferences: Dict[
        str, bool
    ]  # Example: {"newsletter": True, "notifications": False}
    consents: Dict[str, bool]  # Example: {"data_sharing": True, "marketing": False}
    updated_at: datetime


class PreferenceHistory(BaseModel):
    user_id: str
    changes: List[dict]  # List of changes with timestamps


class ConsentArtifact(BaseModel):
    artifact_id: str
    content: str  # Example: JSON or text representation of the artifact


class PreferenceDataExport(BaseModel):
    user_id: str
    export_format: str  # CSV, JSON, etc.
    data: List[dict]


class DPARRequest(BaseModel):
    request_id: str
    user_id: str
    request_type: str  # e.g., "data_access", "data_deletion"
    status: str  # e.g., "pending", "approved", "rejected"
    requested_at: datetime
    processed_at: Optional[datetime]
    documents: Optional[List[str]]  # Document IDs or URLs


class DPARStatusDashboard(BaseModel):
    total_requests: int
    pending_requests: int
    approved_requests: int
    rejected_requests: int


class DPDataExport(BaseModel):
    user_id: str
    data: dict  # Data to be exported


class VerifyEmailResponse(BaseModel):
    verified: bool
    message: str


class VerifyMobileResponse(BaseModel):
    verified: bool
    message: str


class VerifyKYCResponse(BaseModel):
    verified: bool
    message: str


class ReKYCRequest(BaseModel):
    user_id: str
    reason: str
    requested_at: datetime


class DataUpdateRequest(BaseModel):
    request_id: str
    user_id: str
    data: dict
    status: str  # e.g., "pending", "approved", "rejected"
    requested_at: datetime
    processed_at: Optional[datetime]


class DataDeletionRequest(BaseModel):
    request_id: str
    user_id: str
    reason: str
    status: str  # e.g., "pending", "approved", "rejected"
    requested_at: datetime
    processed_at: Optional[datetime]


class DPOAssignment(BaseModel):
    task_id: str
    dpo_id: str
    task_description: str
    status: str  # e.g., "assigned", "in-progress", "completed"


class DPOAudit(BaseModel):
    action_id: str
    action_type: str  # e.g., "approve", "reject", "update"
    performed_by: str
    timestamp: datetime
    details: dict


class DPOComplianceReport(BaseModel):
    total_requests: int
    total_approved: int
    total_rejected: int
    compliance_percentage: float


class DPOFeedback(BaseModel):
    feedback_id: str
    user_id: str
    feedback_text: str
    submitted_at: datetime


class BreachTemplate(BaseModel):
    template_id: str
    title: str
    description: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]


class BreachIncident(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: str  # e.g., "low", "medium", "high"
    reported_at: datetime
    status: str  # e.g., "investigating", "resolved"
    affected_data: List[dict]  # Details about affected data


class BreachNotificationArtifact(BaseModel):
    artifact_id: str
    title: str
    content: str
    published_at: Optional[datetime]


class BreachNotification(BaseModel):
    notification_id: str
    incident_id: str
    recipients: List[str]
    subject: str
    message: str
    sent_at: Optional[datetime]


class DataBreachInvestigation(BaseModel):
    investigation_id: str
    incident_id: str
    investigator: str
    findings: dict
    status: str  # e.g., "ongoing", "completed"
    started_at: datetime
    completed_at: Optional[datetime]


class ScanProfile(BaseModel):
    name: str
    description: Optional[str] = None
    settings: dict  # Scan profile settings (e.g., scan type, frequency, etc.)
    status: str = "inactive"  # e.g., active, inactive, published, unpublished


class UpdateScanProfile(BaseModel):
    name: Optional[str]
    description: Optional[str]
    settings: Optional[dict]
    status: Optional[str]
