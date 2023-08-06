import asyncio
from tqdm import tqdm
from pyferno.exception import PromiseException


class Promise(object):
    @staticmethod
    async def _internal_worker(semaphore, task, idx: int = None, pbar=None):
        """
        This is internal worker that uses semaphore to control concurrency
        :param semaphore:
        :param task:
        :return:
        """
        async with semaphore:
            if pbar and callable(pbar.update):
                pbar.update(1)
            return idx, await task

    @staticmethod
    async def all(__tasks: list, concurrency: int = 20, progress: object = None) -> list:
        """
        Runs thru the list of tasks asynchronously by limiting the concurrency by using a semaphore
        :param __tasks: List of tasks
        :param concurrency: Concurrency of running tasks, integer. Defaults to 10
        :param progress: Progress bar message or boolean True to display default progress bar
        :return: Returns list with finished tasks (fulfilled promises)
        """
        try:
            semaphore = asyncio.Semaphore(concurrency)
            progress_message = ""
            if progress:
                progress_message = progress if isinstance(progress, str) else "Promise.all"
                progress_disabled = False
            else:
                progress_disabled = True

            with tqdm(desc=progress_message, disable=progress_disabled) as pbar:
                tasks = list()
                for _key, _task in enumerate(__tasks):
                    task = Promise._internal_key_worker(semaphore, _key, _task, pbar)
                    tasks.append(task)

                out = [v for (k, v) in await asyncio.gather(*tasks)]
                return out

        except PromiseException as ex:
            print(ex)
            raise

    @staticmethod
    async def _internal_key_worker(semaphore, key, task, pbar=None):
        """
        This is internal worker that uses semaphore to control concurrency
        :param semaphore:
        :param task:
        :return:
        """
        async with semaphore:
            out = await task
            pbar.update(1)
            return key, out

    @staticmethod
    async def props(__props: dict, concurrency: int = 20, progress: object = None) -> dict:
        """
        Runs thru the dict of key,task asynchronously by limiting the concurrency b using a semaphore.
        Maps results back to the dictionary with same keys with all tasks fulfilled.
        It will fail if any task fails
        :param __tasks: Map (dict) with name:task pairs. Task is an async function
        :param concurrency: Concurrency of running tasks, integer. Defaults to 10
        :param progress: Progress bar message or boolean True to display default progress bar
        :return: Returns dict with name:<finished task> pairs.
        """
        try:
            progress_message = ""
            if progress:
                progress_message = progress if isinstance(progress, str) else "Promise.all"
            with tqdm(desc=progress_message) as pbar:
                semaphore = asyncio.Semaphore(concurrency)
                tasks = list()
                for _key, _task in __props.items():
                    task = Promise._internal_key_worker(semaphore, _key, _task, pbar)
                    tasks.append(task)

                out = {k: v for (k, v) in await asyncio.gather(*tasks)}
                return out

        except PromiseException as ex:
            print(ex)
            raise
