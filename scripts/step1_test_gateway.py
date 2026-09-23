# scripts/step1_test_gateway.py
"""步骤 1 验收脚本：验证 LLM 网关能成功调通模型。

在项目根目录运行：
    uv run python -m scripts.step1_test_gateway
"""
import asyncio

from app.core.config import settings
from app.core.llm_gateway import LLMGateway, Msg


async def main() -> None:
    gateway = LLMGateway(settings)

    print(f"接入地址 base_url : {settings.llm_base_url}")
    print(f"调用模型  model   : {gateway.model}")
    print("-" * 50)

    # 消息列表：system 定人设/规则，user 是用户提问（后续还会有 assistant / tool）
    messages = [
        Msg("system", "你是一个乐于助人的技术助手，回答请简洁，不超过两句话。"),
        Msg("user", "请用通俗的语言解释：什么是 RAG（检索增强生成）？"),
    ]

    print("提问中，等待模型回复 ...\n")
    result = await gateway.chat(messages)

    print("模型回复：")
    print(result.text)
    print("-" * 50)
    print(f"prompt tokens     : {result.prompt_tokens}")
    print(f"completion tokens : {result.completion_tokens}")
    print(f"总 tokens         : {result.prompt_tokens + result.completion_tokens}")
    print(f"耗时 latency      : {result.latency_ms} ms")


if __name__ == "__main__":
    asyncio.run(main())
