"""Utilitizes."""

import asyncio
import sys

from typing import Awaitable

import eventkit as ev

globalErrorEvent = ev.Event()

def run(*awaitables: Awaitable, timeout: float = None):
    """
    By default run the event loop forever.
    When awaitables (like Tasks, Futures or coroutines) are given then
    run the event loop until each has completed and return their results.
    An optional timeout (in seconds) can be given that will raise
    asyncio.TimeoutError if the awaitables are not ready within the
    timeout period.
    """
    loop = asyncio.get_event_loop()
    if not awaitables:
        if loop.is_running():
            return
        loop.run_forever()
        result = None
        all_tasks = (
            asyncio.all_tasks(loop)  # type: ignore
            if sys.version_info >= (3, 7) else asyncio.Task.all_tasks())
        if all_tasks:
            # cancel pending tasks
            f = asyncio.gather(*all_tasks)
            f.cancel()
            try:
                loop.run_until_complete(f)
            except asyncio.CancelledError:
                pass
    else:
        if len(awaitables) == 1:
            future = awaitables[0]
        else:
            future = asyncio.gather(*awaitables)
        if timeout:
            future = asyncio.wait_for(future, timeout)
        task = asyncio.ensure_future(future)

        def onError(_):
            task.cancel()

        globalErrorEvent.connect(onError)
        try:
            result = loop.run_until_complete(task)
        except asyncio.CancelledError as e:
            raise globalErrorEvent.value() or e
        finally:
            globalErrorEvent.disconnect(onError)

    return result
