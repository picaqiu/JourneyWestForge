# AI Native Track

This directory grows JourneyWestForge from a collection of Java experiments into an interview-defensible production AI platform.

## Boundary

- **Java control plane (planned, Java 21):** authentication, tenant, quota, research-task lifecycle, report API, transactional outbox.
- **Python agent runtime (started, Python 3.12):** planning, tool execution, RAG, MCP, checkpointing, evaluation.
- **Contracts:** language-neutral API, event, and tool schemas.
- **Infrastructure (planned):** PostgreSQL + pgvector, Redis, Kafka, OpenTelemetry.

Java and Python must not write each other's owned tables. Long-running work crosses the boundary through versioned events; synchronous HTTP remains for health, control, and query paths.

## Current layout

```text
ai-native/
├── contracts/                 # Language-neutral schemas
├── docs/
│   ├── adr/                   # Architecture decisions
│   ├── ARCHITECTURE_REVIEW.md
│   └── EXPERIMENTS.md
└── python-agent-runtime/
    ├── src/journeywest_agent/
    └── tests/
```

## Run the first experiments

```bash
cd python-agent-runtime
python3 -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

No model key, Kafka, Redis, or database is required for the first two experiments. That is deliberate: they isolate contract correctness and async failure semantics before infrastructure is introduced.

## Learning workflow

For each experiment:

1. Read its hypothesis and failure scenario in `docs/EXPERIMENTS.md`.
2. Predict the result before running the test.
3. Run the focused test and explain the output.
4. Change one variable and rerun it.
5. Write the conclusion and its limits.
6. Defend the decision without looking at the implementation.

Do not claim an experiment in an interview until you can reproduce it and explain why the test proves the conclusion.
