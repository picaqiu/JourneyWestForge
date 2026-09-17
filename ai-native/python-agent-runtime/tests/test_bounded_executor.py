import asyncio
from unittest import IsolatedAsyncioTestCase

from journeywest_agent.runtime.bounded_executor import (
    BoundedAsyncExecutor,
    ExecutionPolicy,
)


class BoundedAsyncExecutorTest(IsolatedAsyncioTestCase):
    async def test_preserves_order_and_caps_concurrency(self) -> None:
        active = 0
        max_active = 0
        counter_lock = asyncio.Lock()

        async def operation(value: int) -> int:
            nonlocal active, max_active
            async with counter_lock:
                active += 1
                max_active = max(max_active, active)
            try:
                await asyncio.sleep(0.01)
                return value * 10
            finally:
                async with counter_lock:
                    active -= 1

        executor = BoundedAsyncExecutor[int, int](
            ExecutionPolicy(max_concurrency=2, overall_timeout_seconds=1.0)
        )

        result = await executor.run([3, 1, 2, 4], operation)

        self.assertEqual([30, 10, 20, 40], result)
        self.assertLessEqual(max_active, 2)

    async def test_failure_cancels_and_cleans_up_sibling(self) -> None:
        slow_started = asyncio.Event()
        slow_cleaned_up = asyncio.Event()

        async def operation(name: str) -> str:
            if name == "slow":
                slow_started.set()
                try:
                    await asyncio.sleep(10)
                finally:
                    slow_cleaned_up.set()
                return name

            await slow_started.wait()
            raise RuntimeError("controlled tool failure")

        executor = BoundedAsyncExecutor[str, str](
            ExecutionPolicy(max_concurrency=2, overall_timeout_seconds=1.0)
        )

        with self.assertRaises(ExceptionGroup) as raised:
            await executor.run(["slow", "fail"], operation)

        self.assertTrue(
            any(isinstance(error, RuntimeError) for error in raised.exception.exceptions)
        )
        self.assertTrue(slow_cleaned_up.is_set())

    async def test_overall_timeout_cancels_running_operation(self) -> None:
        started = asyncio.Event()
        cleaned_up = asyncio.Event()

        async def operation(_: int) -> int:
            started.set()
            try:
                await asyncio.sleep(10)
            finally:
                cleaned_up.set()
            return 1

        executor = BoundedAsyncExecutor[int, int](
            ExecutionPolicy(max_concurrency=1, overall_timeout_seconds=0.03)
        )

        with self.assertRaises(TimeoutError):
            await executor.run([1], operation)

        self.assertTrue(started.is_set())
        self.assertTrue(cleaned_up.is_set())

    async def test_operation_timeout_fails_batch_and_runs_cleanup(self) -> None:
        cleaned_up = asyncio.Event()

        async def operation(_: int) -> int:
            try:
                await asyncio.sleep(10)
            finally:
                cleaned_up.set()
            return 1

        executor = BoundedAsyncExecutor[int, int](
            ExecutionPolicy(
                max_concurrency=1,
                overall_timeout_seconds=1.0,
                operation_timeout_seconds=0.03,
            )
        )

        with self.assertRaises(ExceptionGroup) as raised:
            await executor.run([1], operation)

        self.assertTrue(
            any(isinstance(error, TimeoutError) for error in raised.exception.exceptions)
        )
        self.assertTrue(cleaned_up.is_set())

    async def test_rejects_invalid_policy(self) -> None:
        with self.assertRaises(ValueError):
            ExecutionPolicy(max_concurrency=0, overall_timeout_seconds=1.0)
