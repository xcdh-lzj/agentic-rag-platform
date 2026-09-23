# app/core/llm_gateway.py
"""统一 LLM 网关 —— 整个项目的地基。

步骤 1（当前）：最小可用版本，。只做一件事——把一次对话调用跑通，并带回 token/耗时

为什么所有模型调用都要经过这一层，而不是在业务代码里直接 import OpenAI？
  1. 一套代码对接任意「OpenAI 兼容」服务：本地 Ollama、DeepSeek、通义、智谱、vLLM……
  2. 重试、降级、熔断、计费统计都能统一加在这一处（步骤 2 会逐步加上）。
  3. 业务代码只依赖 Msg / GenResult 这两个稳定的数据结构，不绑定具体 SDK。
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Literal

from openai import AsyncOpenAI

from app.core.config import Settings

Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class Msg:
    """一条聊天消息，role / content 与 OpenAI 协议完全一致。"""

    role: Role
    content: str


@dataclass
class GenResult:
    """一次生成的结果 + 计量信息（成本、延迟统计都靠它）。"""

    text: str
    prompt_tokens: int
    completion_tokens: int
    model: str
    latency_ms: int


class LLMGateway:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model = settings.llm_model
        # AsyncOpenAI 是 OpenAI 官方异步客户端；任何兼容协议的服务都能这样接入
        self._client = AsyncOpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            timeout=settings.llm_timeout,
        )

    async def chat(
        self,
        messages: list[Msg],
        *,
        temperature: float | None = None,
        **kwargs,
    ) -> GenResult:
        """非流式对话：发送消息列表，返回完整回复与 token 统计。"""
        t0 = time.perf_counter()

        resp = await self._client.chat.completions.create(
            model=self.model,
            # dataclass 转 dict：{"role": ..., "content": ...}
            messages=[m.__dict__ for m in messages],
            temperature=(
                self.settings.llm_temperature if temperature is None else temperature
            ),
            **kwargs,
        )

        usage = resp.usage
        return GenResult(
            text=resp.choices[0].message.content or "",
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            model=self.model,
            latency_ms=int((time.perf_counter() - t0) * 1000),
        )
