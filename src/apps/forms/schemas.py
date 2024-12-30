import datetime
from sqlalchemy import Column, String, JSON, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from typing import Literal, List, Dict
from src.db import Base

class Form(Base):
    __tablename__ = "forms"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    fields = Column(JSON, nullable=False)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    form_id = Column(UUID(as_uuid=True), nullable=False)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    data = Column(JSON, nullable=False)

class FieldSchema(BaseModel):
    field_id: str
    type: Literal["string", "number", "boolean"]
    label: str
    required: bool

class FormCreate(BaseModel):
    title: str
    description: str
    fields: List[FieldSchema]

class SubmissionResponse(BaseModel):
    submission_id: str
    submitted_at: str
    data: Dict[str, str]

class SubmissionListResponse(BaseModel):
    total_count: int
    page: int
    limit: int
    submissions: List[SubmissionResponse]