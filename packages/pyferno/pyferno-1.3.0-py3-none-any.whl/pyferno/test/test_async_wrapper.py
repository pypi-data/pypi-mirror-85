import pytest
import asyncio
import random
from pyferno.util import async_wrapper


@pytest.mark.tryfirst
def test_async_wrapper():
    async def async_method():
        await asyncio.sleep(0.3)
        return random.randint(1000, 9999)

    out = async_wrapper(async_method)
    assert out > 0
    print(out)
