# Python Agent Runtime Foundation

The first slice isolates two production concerns before any LLM framework is introduced:

1. strict, versioned contracts at the Java / Python boundary;
2. bounded async execution with fail-fast cancellation and cleanup.

## Requirements

- Python 3.12+
- Pydantic 2.x

## Run

```bash
python3 -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Deliberate non-goals

- no FastAPI endpoint yet;
- no real LLM SDK yet;
- no LangGraph yet;
- no Kafka client yet.

Those dependencies would make the first experiments less deterministic. They enter only when the contract and cancellation behavior are proven.
