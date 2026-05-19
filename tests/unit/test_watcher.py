# tests/unit/test_watcher.py

import asyncio
from pathlib import Path

import pytest

from pylings.core.watcher import watch


@pytest.mark.asyncio
async def test_watcher_yields_on_change(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("v1\n", encoding="utf-8")

    received: list[None] = []

    async def consume() -> None:
        async for _ in watch(file, debounce_ms=50):
            received.append(None)
            if len(received) >= 1:
                break

    task = asyncio.create_task(consume())
    await asyncio.sleep(0.2)
    file.write_text("v2\n", encoding="utf-8")
    await asyncio.wait_for(task, timeout=3.0)
    assert len(received) == 1


@pytest.mark.asyncio
async def test_watcher_debounces_burst(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("v1\n", encoding="utf-8")

    received: list[None] = []

    async def consume() -> None:
        async for _ in watch(file, debounce_ms=200):
            received.append(None)

    task = asyncio.create_task(consume())
    await asyncio.sleep(0.2)
    for i in range(5):
        file.write_text(f"v{i}\n", encoding="utf-8")
        await asyncio.sleep(0.02)
    await asyncio.sleep(0.6)
    task.cancel()
    assert 1 <= len(received) <= 2, f"expected debounced, got {len(received)} events"
