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
