# Production AI Experiment Registry

An experiment is complete only when it has a hypothesis, controlled failure, automated evidence, recorded result, and an interview explanation.

| ID | Status | Experiment | Question answered | Required evidence |
|---|---|---|---|---|
| EXP-001 | Implemented | Contract boundary | Can invalid or incompatible task events be rejected before entering runtime logic? | Pydantic tests + versioned JSON Schema |
| EXP-002 | Implemented | Bounded async execution | Is concurrency capped, and do timeout / failure cancel siblings while running cleanup? | deterministic async tests |
| EXP-003 | Planned | Transactional outbox | What happens between DB commit and Kafka publish? | crash-window integration tests |
| EXP-004 | Planned | Idempotent consumer | Can a task event be replayed 20 times without duplicate side effects? | replay test + state evidence |
| EXP-005 | Planned | LLM adapter reliability | Which timeout / 429 / malformed-response failures are retryable? | fake HTTP server + error taxonomy |
| EXP-006 | Planned | RAG baseline | How well does simple dense retrieval work before optimization? | golden set + Recall@K + failure cases |
| EXP-007 | Planned | Chunk / hybrid / rerank | Which change improves retrieval, and at what latency / token cost? | one-variable experiment table |
| EXP-008 | Planned | Agent checkpoint | Can a run resume after process death without repeating a tool side effect? | kill / resume test + audit records |
| EXP-009 | Planned | MCP trust boundary | Are invalid, unauthorized, or high-risk tool calls rejected and audited? | schema / auth / approval tests |
| EXP-010 | Planned | Cross-runtime trace | Can one trace follow Java → Kafka → Python → RAG / MCP? | trace screenshot + propagated IDs |

## EXP-001: Contract boundary

### Hypothesis

Strict boundary models with `extra=forbid`, explicit enums, semantic validators, and a versioned language-neutral schema prevent malformed messages from becoming ambiguous runtime failures.

### Run

```bash
cd ai-native/python-agent-runtime
PYTHONPATH=src python3 -m unittest tests.test_models tests.test_contract_alignment -v
```

### Change one variable

Temporarily remove `extra="forbid"`, send an unknown field, and explain why accepting it can hide producer / consumer drift.

### Interview questions

1. Which schema changes are backward compatible?
2. Why is JSON Schema not sufficient for every business invariant?
3. Where should poison events go?

## EXP-002: Bounded async execution

### Hypothesis

Structured concurrency plus explicit semaphores and deadlines prevents unbounded tool fan-out, orphaned tasks, and leaked resources.

### Run

```bash
cd ai-native/python-agent-runtime
PYTHONPATH=src python3 -m unittest tests.test_bounded_executor -v
```

### Controlled failures

- submit more operations than the concurrency limit;
- let one sibling raise while another is sleeping;
- let the overall deadline expire;
- verify `finally` cleanup executes.

### Change one variable

Replace `TaskGroup` with `gather` and predict which siblings continue after the first exception. Then measure rather than relying on memory.

### Interview questions

1. Why is `async def` alone not a concurrency policy?
2. How does cancellation propagate through an Agent run?
3. What should happen to an external tool call that already produced a side effect?

## Next implementation order

1. Add the standalone Java 21 control plane with task + outbox.
2. Add Kafka and complete EXP-003 / EXP-004.
3. Add the provider-neutral LLM adapter and fake HTTP server.
4. Establish the RAG baseline before introducing LangGraph.
5. Hand-write the Agent state machine before migrating it to a framework.
