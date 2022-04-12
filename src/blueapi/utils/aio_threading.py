import asyncio
from asyncio import Future as AioFuture
from concurrent.futures import Future as ConcurrentFuture
from typing import Optional


def concurrent_future_to_aio_future(
    concurrent_future: ConcurrentFuture,
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> AioFuture:
    aio_future: AioFuture = AioFuture(loop=loop)

    def transcribe(future: ConcurrentFuture) -> None:
        ex = future.exception()
        if ex is not None:
            aio_future.set_exception(ex)
        rs = future.result()
        if rs is not None:
            aio_future.set_result(rs)

    def on_complete(future: ConcurrentFuture) -> None:
        aio_future.get_loop().call_soon_threadsafe(transcribe, future)

    concurrent_future.add_done_callback(on_complete)

    return aio_future