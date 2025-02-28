from jupyter_ai_magics import BaseProvider
from langchain_community.llms.fake import FakeStreamingListLLM, FakeListLLM
from jijzept_agent_client.jijzept_agent import CustomLLMStreamingAsync
from jupyter_ai import (
    InlineCompletionRequest,
    InlineCompletionReply,
    InlineCompletionList,
    InlineCompletionStreamChunk,
)

from asyncio import FIRST_COMPLETED, Task, create_task, wait, sleep
import os
from typing import AsyncIterable, AsyncIterator, Collection, TypeVar
from jupyter_ai_magics import BaseEmbeddingsProvider
from jijzept_agent_client.jijzept_agent import CustomLLMEmbbeding


_T = TypeVar("_T")


async def _await_next(iterator: AsyncIterator[_T]) -> _T:
    return await iterator.__anext__()


def _as_task(iterator: AsyncIterator[_T]) -> Task[_T]:
    return create_task(_await_next(iterator))


async def merge_iterators(
    iterators: Collection[AsyncIterator[_T]],
) -> AsyncIterable[_T]:
    next_tasks = {iterator: _as_task(iterator) for iterator in iterators}
    while next_tasks:
        done, _ = await wait(next_tasks.values(), return_when=FIRST_COMPLETED)
        for task in done:
            iterator = next(it for it, t in next_tasks.items() if t == task)
            try:
                yield task.result()
            except StopAsyncIteration:
                del next_tasks[iterator]
            except Exception:
                pass
            else:
                next_tasks[iterator] = _as_task(iterator)


class MyProvider(BaseProvider, FakeListLLM):
    id = "my_provider"
    name = "My Provider"
    model_id_key = "model"
    models = ["model_a", "model_b"]

    def __init__(self, **kwargs):
        model = kwargs.get("model_id")
        kwargs["responses"] = (
            ["This is a response from model 'a'"]
            if model == "model_a"
            else ["This is a response from model 'b'"]
        )
        super().__init__(**kwargs)


class MyEmbeddingsProvider(BaseEmbeddingsProvider, CustomLLMEmbbeding):
    id = "my_embeddings_provider"
    name = "My Embeddings Provider"
    model_id_key = "model"
    models = ["my_model"]

    def __init__(self, **kwargs):
        # Get server URL from environment variable or use localhost as default
        server_url = os.environ.get("JIJZEPT_SERVER_URL", "http://localhost:8000")
        kwargs["server_url"] = server_url
        super().__init__(size=300, **kwargs)


class MyCompletionProvider(BaseProvider, CustomLLMStreamingAsync):
    id = "my_provider"
    name = "My Provider2"
    model_id_key = "model"
    models = ["model_a"]

    def __init__(self, **kwargs):
        # Get server URL from environment variable or use localhost as default
        server_url = os.environ.get("JIJZEPT_SERVER_URL", "http://localhost:8000")
        kwargs["server_url"] = server_url
        super().__init__(**kwargs)
