# pylings/core/watcher.py

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from watchfiles import awatch


async def watch(path: Path, debounce_ms: int = 100) -> AsyncIterator[None]:
    """Yield once each time `path` changes. Debounce coalesces bursty saves."""
    async for _changes in awatch(path, debounce=debounce_ms, recursive=False):
        yield None
