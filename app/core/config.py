# app/core/config.py
"""全局配置：所有密钥 / 地址 / 参数都从 .env 读取，代码里不写死任何密钥。

使用 pydantic-settings：
  · 自动读取项目根目录的 .env
  · 自动做类型校验（地址是 str、超时是 float）
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",          # .env 里多写的字段不报错
    )

    # ---- 主模型（OpenAI 兼容协议：Ollama / DeepSeek / 通义 / 智谱 / Kimi / vLLM 都能接）----
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"          # 本地 Ollama 随便填；云端填 sk-xxx
    llm_model: str = "deepseek-r1:8b"
    llm_timeout: float = 120.0
    llm_temperature: float = 0.1         # 事实型问答用低温，降低随机性

    # ---- 备用模型（步骤 2 启用降级链，留空则暂不降级）----
    llm_backup_base_url: str = ""
    llm_backup_api_key: str = ""
    llm_backup_model: str = ""


# 全局单例：其它文件直接 `from app.core.config import settings`
settings = Settings()
