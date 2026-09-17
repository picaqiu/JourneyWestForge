from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

InputT = TypeVar("InputT")
ResultT = TypeVar("ResultT")


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    """Resource and deadline limits for one batch of async operations."""

    max_concurrency: int
    overall_timeout_seconds: float
    operation_timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        if self.max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")
        if self.overall_timeout_seconds <= 0:
            raise ValueError("overall_timeout_seconds must be positive")
        if self.operation_timeout_seconds is not None and self.operation_timeout_seconds <= 0:
            raise ValueError("operation_timeout_seconds must be positive when provided")


class BoundedAsyncExecutor(Generic[InputT, ResultT]):
    """Runs independent operations with structured, fail-fast concurrency.

    TaskGroup owns every child task. If one operation fails, its siblings are
    cancelled and awaited before this method raises. The outer timeout applies
    to the entire batch, including time spent waiting for the semaphore.
    """

    def __init__(self, policy: ExecutionPolicy) -> None:
        self._policy = policy

    async def run(
        self,
        items: Sequence[InputT],
        operation: Callable[[InputT], Awaitable[ResultT]],
    ) -> list[ResultT]:
        if not items:
            return []

        semaphore = asyncio.Semaphore(self._policy.max_concurrency)
        results: list[ResultT | None] = [None] * len(items)

        async def invoke(index: int, item: InputT) -> None:
            async with semaphore:
                if self._policy.operation_timeout_seconds is None:
                    results[index] = await operation(item)
                    return

                async with asyncio.timeout(self._policy.operation_timeout_seconds):
                    results[index] = await operation(item)

        async with asyncio.timeout(self._policy.overall_timeout_seconds):
            async with asyncio.TaskGroup() as task_group:
                for index, item in enumerate(items):
                    task_group.create_task(invoke(index, item))

        return cast(list[ResultT], results)
