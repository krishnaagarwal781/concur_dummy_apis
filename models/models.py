from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId


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