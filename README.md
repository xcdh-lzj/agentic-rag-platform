# 企业级 Agentic RAG 知识库问答平台（教学项目）

面向企业私有文档（合同 / 制度 / 技术手册 / 工单），实现 **文档解析 → 语义切分 → 混合召回 → 重排 → 引证生成 → Agentic 编排 → 自动化评测** 的全链路。

本仓库按「教学模式」分步推进，每一步都可独立运行、验证，再进入下一步。

## 环境准备

- [uv](https://docs.astral.sh/uv/)（包管理，已安装）
- Python 3.11（由 uv 自动管理，无需手动安装）
- 一个 OpenAI 兼容的模型服务（默认用本地 Ollama，零成本）

依赖已在初始化时安装完成。如需重装：

```bash
uv sync
```

## 模型配置

配置统一放在项目根目录的 `.env`（已默认配好本地 Ollama）。
如需切换 DeepSeek / 智谱 / 通义 / Kimi，参考 `.env.example` 中的模板。

> 用本地 Ollama 前，确保服务已启动：`ollama serve`（或已通过 `ollama pull deepseek-r1:8b` 下载模型）。

## 步骤 1：项目骨架 + 配置管理 + LLM 网关

目标：跑通一次模型调用，理解「统一网关」的作用，并看懂 token / 延迟统计。

```bash
uv run python -m scripts.step1_test_gateway
```

预期输出：模型对「什么是 RAG」的解释，以及 prompt/completion tokens 和耗时。

## 当前项目结构

```
agentic-rag-platform/
├── app/
│   └── core/
│       ├── config.py          # 配置：从 .env 读取（pydantic-settings）
│       └── llm_gateway.py     # 统一 LLM 网关（步骤1：最小可用版本）
├── scripts/
│   └── step1_test_gateway.py  # 步骤1 验收脚本
├── .env                       # 实际配置（不提交 git）
├── .env.example               # 各模型配置模板
└── pyproject.toml
```

## 学习路线（后续步骤）

1. 项目骨架 + 配置 + LLM 网关（当前）
2. LLM 网关增强：重试 / 降级 / 熔断 / 统计
3. 文档解析器（PDF/MD/DOCX → Block）
4. 结构感知切分（Small-to-Big）
5. BGE-M3 向量化 + 向量库入库
6. 混合检索 + RRF
7. Rerank 重排
8. 引证生成 + 拒答
9. FastAPI + SSE
10. RAGAS 评测
11. 消融实验
12. LangGraph Agentic 状态机
13. 多轮对话
14. 权限隔离 + 缓存
15. Docker 部署 + 压测 + 简历
