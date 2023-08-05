from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Awaitable, Generator, List, Union

if TYPE_CHECKING:
    from logging import Logger


def ensure_future_with_log(cor: Union[Generator, Awaitable],
                           *,
                           logger: Logger,
                           message: str) -> None:

    def _done_callback(fut: asyncio.Task) -> None:
        try:
            fut.result()
        except Exception:
            logger.warn(message, exc_info=True)

    asyncio.create_task(cor) \
        .add_done_callback(_done_callback)


async def gather_with_log(coros: List[Union[Generator, Awaitable]],
                          *,
                          logger: Logger) -> None:
    task_results = await asyncio.gather(*coros, return_exceptions=True)
    for result in task_results:
        try:
            if isinstance(result, Exception):
                raise result
        except Exception:
            logger.warn('Error from asyncio.gather()', exc_info=True)
