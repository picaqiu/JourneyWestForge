from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictBoundaryModel(BaseModel):
    """Base type for data crossing a process or language boundary."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    PLANNING = "PLANNING"
    RUNNING = "RUNNING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ResearchTaskCreate(StrictBoundaryModel):
    tenant_id: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$",
    )
    query: str = Field(min_length=1, max_length=4000)
    requested_by: str = Field(min_length=1, max_length=128)
    idempotency_key: str = Field(min_length=8, max_length=128)


class TaskSubmittedPayload(StrictBoundaryModel):
    query: str = Field(min_length=1, max_length=4000)
    requested_by: str = Field(min_length=1, max_length=128)
    idempotency_key: str = Field(min_length=8, max_length=128)


class ResearchTaskSubmittedEvent(StrictBoundaryModel):
    schema_version: Literal["1.0"]
    event_id: UUID
    event_type: Literal["research.task.submitted"]
    occurred_at: datetime
    trace_id: str = Field(
        min_length=16,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    tenant_id: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$",
    )
    task_id: UUID
    payload: TaskSubmittedPayload

    @field_validator("occurred_at")
    @classmethod
    def normalize_utc_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must include a timezone")
        return value.astimezone(timezone.utc)


class Citation(StrictBoundaryModel):
    document_id: UUID
    document_version: int = Field(ge=1)
    source_uri: str = Field(min_length=1, max_length=2048)
    source_start: int = Field(ge=0)
    source_end: int = Field(gt=0)
    quote: str = Field(min_length=1, max_length=4000)

    @model_validator(mode="after")
    def validate_source_span(self) -> Citation:
        if self.source_end <= self.source_start:
            raise ValueError("source_end must be greater than source_start")
        return self
