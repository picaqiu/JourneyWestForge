import json
from pathlib import Path
from unittest import TestCase

from journeywest_agent.domain.models import ResearchTaskSubmittedEvent, TaskSubmittedPayload


class ContractAlignmentTest(TestCase):
    def test_static_event_contract_matches_required_model_fields(self) -> None:
        contract_path = (
            Path(__file__).resolve().parents[2]
            / "contracts"
            / "research-task-submitted.v1.schema.json"
        )
        contract = json.loads(contract_path.read_text(encoding="utf-8"))

        required_by_contract = set(contract["required"])
        required_by_model = {
            name
            for name, field in ResearchTaskSubmittedEvent.model_fields.items()
            if field.is_required()
        }

        self.assertEqual(required_by_model, required_by_contract)
        self.assertFalse(contract["additionalProperties"])
        self.assertEqual("1.0", contract["properties"]["schema_version"]["const"])
        self.assertEqual(
            "research.task.submitted",
            contract["properties"]["event_type"]["const"],
        )

        payload_contract = contract["properties"]["payload"]
        required_payload_fields = {
            name
            for name, field in TaskSubmittedPayload.model_fields.items()
            if field.is_required()
        }
        self.assertEqual(required_payload_fields, set(payload_contract["required"]))
        self.assertFalse(payload_contract["additionalProperties"])
