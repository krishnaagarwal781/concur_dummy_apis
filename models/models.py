from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId


class App(BaseModel):
    name: str
    description: Optional[str]
    status: str = "draft"  # draft, published, unpublished


class UpdateApp(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]


# Collection point management models
class CollectionPoint(BaseModel):
    name: str
    description: Optional[str]
    status: str = "draft"  # draft, published, unpublished


class UpdateCollectionPoint(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]


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
    template_name: str
    content: str
    status: str = "draft"  # draft, published, unpublished


class UpdateModelNotice(BaseModel):
    template_name: Optional[str]
    content: Optional[str]
    status: Optional[str]


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
