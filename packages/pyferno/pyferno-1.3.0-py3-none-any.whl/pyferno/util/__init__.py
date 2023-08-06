import asyncio
from asyncio import coroutine


def async_wrapper(async_method: coroutine, *args, **kwargs):
    """
    This is a helper method to run async methods in sync context
    here and there
    :param async_method:
    :return:
    """
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(async_method(*args, **kwargs))
    loop.close()
    return out
