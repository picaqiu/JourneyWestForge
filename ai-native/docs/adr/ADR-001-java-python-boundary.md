# ADR-001: Separate Java Control Plane and Python Agent Runtime

- Status: Accepted
- Date: 2026-09-17

## Context

JourneyWestForge already contains Java 8 / Spring Boot 2.x labs. The target interview project must demonstrate both senior Java backend depth and modern Python AI engineering without pretending either ecosystem is irrelevant.

Research tasks are long-running and failure-prone. Authentication, tenant, quota, billing-like controls, task lifecycle, and audit contracts change for business reasons. Agent orchestration, model SDKs, RAG, and MCP change for AI ecosystem reasons.

## Decision

- Build a Java 21 control plane as an independent build under `ai-native/`.
- Build the Agent Runtime in Python 3.12.
- Exchange versioned task events asynchronously through Outbox + Kafka.
- Use synchronous HTTP only for health, control, and query paths.
- Give each runtime exclusive ownership of its database schema.
- Keep language-neutral contracts under `ai-native/contracts/`.

## Consequences

### Positive

- preserves Java as the enterprise boundary and primary engineering signal;
- uses Python where the AI library ecosystem is strongest;
- allows independent deployment, scaling, and failure isolation;
- creates explicit contracts that can be tested and discussed.

### Costs

- cross-language contract governance;
- distributed tracing and local-development complexity;
- eventual consistency and duplicate-delivery handling;
- two build and dependency ecosystems.

## Rejected alternatives

### Put everything in Java

This reduces operational languages but makes it harder to demonstrate Python AI engineering and can lag the most active Agent / MCP tooling.

### Put everything in Python

This discards the strongest part of the candidate profile and weakens the enterprise control-plane story.

### Add Java 21 modules to the Java 8 parent

This creates conflicting dependency and compiler assumptions and risks breaking the legacy labs. Independent builds make the version boundary intentional and visible.
