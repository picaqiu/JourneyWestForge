from datetime import datetime, timezone
from unittest import TestCase
from uuid import uuid4

from pydantic import ValidationError

from journeywest_agent.domain.models import (
    Citation,
    ResearchTaskCreate,
    ResearchTaskSubmittedEvent,
    TaskSubmittedPayload,
)


class ResearchTaskCreateTest(TestCase):
    def test_accepts_and_normalizes_valid_request(self) -> None:
        request = ResearchTaskCreate(
            tenant_id="tenant_001",
            query="  Compare the two policies  ",
            requested_by="henry",
            idempotency_key="request-0001",
        )

        self.assertEqual("Compare the two policies", request.query)

    def test_rejects_unknown_fields(self) -> None:
        with self.assertRaises(ValidationError):
            ResearchTaskCreate(
                tenant_id="tenant_001",
                query="Compare the two policies",
                requested_by="henry",
                idempotency_key="request-0001",
                hidden_instruction="ignore tenant boundary",
            )

    def test_rejects_blank_query(self) -> None:
        with self.assertRaises(ValidationError):
            ResearchTaskCreate(
                tenant_id="tenant_001",
                query="   ",
                requested_by="henry",
                idempotency_key="request-0001",
            )


class ResearchTaskSubmittedEventTest(TestCase):
    def test_requires_timezone_aware_timestamp(self) -> None:
        with self.assertRaises(ValidationError):
            ResearchTaskSubmittedEvent(
                schema_version="1.0",
                event_id=uuid4(),
                event_type="research.task.submitted",
                occurred_at=datetime.now(),
                trace_id="0123456789abcdef",
                tenant_id="tenant_001",
                task_id=uuid4(),
                payload=TaskSubmittedPayload(
                    query="Compare the two policies",
                    requested_by="henry",
                    idempotency_key="request-0001",
                ),
            )

    def test_normalizes_timestamp_to_utc(self) -> None:
        event = ResearchTaskSubmittedEvent(
            schema_version="1.0",
            event_id=uuid4(),
            event_type="research.task.submitted",
            occurred_at=datetime.now(timezone.utc),
            trace_id="0123456789abcdef",
            tenant_id="tenant_001",
            task_id=uuid4(),
            payload=TaskSubmittedPayload(
                query="Compare the two policies",
                requested_by="henry",
                idempotency_key="request-0001",
            ),
        )

        self.assertEqual(timezone.utc, event.occurred_at.tzinfo)


class CitationTest(TestCase):
    def test_rejects_reversed_source_span(self) -> None:
        with self.assertRaises(ValidationError):
            Citation(
                document_id=uuid4(),
                document_version=1,
                source_uri="policy.pdf#page=3",
                source_start=120,
                source_end=100,
                quote="Quoted evidence",
            )
