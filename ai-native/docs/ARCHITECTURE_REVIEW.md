# JourneyWestForge Architecture Review

Review baseline: commit `7fb649f`, 2026-09-17.

## Executive assessment

The repository is a useful **architecture-lab seed**, but it is not yet a portfolio project that can sustain a 45–60 minute senior interview deep dive.

At the reviewed commit it contains 17 Maven POM files and 9 Java source files. Several named modules are currently structure-only. The strongest existing material is:

- JMH experiments around dead-code elimination and benchmark correctness;
- the beginning of a custom RPC protocol abstraction;
- a module map covering JVM, performance, RPC, microservices, and system-design exercises.

The main gap is not the number of technologies. It is the lack of an end-to-end business path, automated failure evidence, reproducible builds, architectural decisions, and measured results.

## What should be kept

1. **The forge / laboratory concept.** It naturally supports experiment-driven interview preparation.
2. **JMH work.** This can become strong JVM material once the benchmark build, raw results, environment, and conclusions are reproducible.
3. **Custom RPC work.** It can demonstrate protocol, proxy, serialization, service discovery, timeout, correlation, and backpressure—if completed through an end-to-end call.
4. **Java 8 track.** It remains useful for legacy systems and Java interview fundamentals.

## Highest-priority gaps

### 1. Breadth currently exceeds depth

Modules such as ID generator, short URL, IM, feed, microservices, and Web3 are mostly empty. Empty module names do not create interview evidence and can invite questions the repository cannot answer.

**Action:** mark them explicitly as backlog or complete one vertical slice before adding another module.

### 2. The repository is not reproducible yet

- no Maven wrapper at the reviewed commit;
- no CI before this change;
- root README previously contained only one sentence;
- no recorded JDK / Maven matrix or benchmark result files;
- the current execution environment does not have Maven installed, so the Java reactor could not be verified here.

**Action:** add a wrapper or documented toolchain, CI, exact run commands, and captured results.

### 3. The legacy parent should not own the AI-native runtime

The existing reactor targets Java 8 and Spring Boot 2.7. A modern control plane should use an independently versioned Java 21 build. Upgrading the root in place would risk breaking the legacy labs and hiding an important compatibility decision.

**Action:** keep `ai-native/` independent and add its Java 21 control plane as a separate build.

### 4. Dependency governance needs cleanup

The parent manages several old libraries, including old Fastjson, Guava, Netty, JUnit, and Protobuf versions. Some may not be used, but carrying them in a portfolio parent still creates avoidable security and maintenance questions.

**Action:** inventory actual use, remove unused managed dependencies, run a dependency / CVE scan, and document why any old version remains.

### 5. RPC DTOs are not yet a wire protocol

`Class<?>[]`, `Object[]`, and `Throwable` are convenient local Java representations but create coupling and unsafe or non-portable serialization choices. The current request / response types also lack correlation ID, protocol version, deadline, status code, attachments, and explicit serializer.

**Action:** design a framed protocol and prove request correlation, timeout, partial reads, malformed frames, backpressure, and serialization compatibility.

### 6. JMH claims need measured evidence

Comments currently predict exact optimization behavior and mention a `benchmarks.jar`, but the module does not yet show a reproducible benchmark packaging configuration or checked-in result report. JIT behavior must be measured rather than asserted.

**Action:** configure a standard JMH build, record JVM flags and environment, run forks, save JSON results, and compare generated assembly where appropriate.

## Recommended repository narrative

Use one sentence in interviews:

> JourneyWestForge is my experiment-driven architecture repository: the Java track isolates JVM, performance, and RPC mechanisms, while the AI-native track assembles those engineering principles into a production-oriented research-agent platform.

This narrative is stronger than presenting every empty directory as a completed system.

## Implementation decision from this review

The first added experiments deliberately avoid LLM providers and infrastructure:

1. strict cross-language task-event contracts;
2. bounded async execution, failure propagation, timeout, and cleanup.

These are prerequisites for a reliable Agent Runtime and can be tested deterministically. Kafka, RAG, LangGraph, and MCP are added only after these semantics are understood.
