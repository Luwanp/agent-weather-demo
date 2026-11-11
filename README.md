# 极简天气 Agent 及评测 Demo

## 项目简介
基于OpenAI兼容接口（DeepSeek）开发的最小可用 Agent 框架。实现了大模型的 Function Calling 机制，并自带自动化评测脚本。

## 核心技术点
1. **Function Calling**：实现大模型根据用户意图自动提取参数并调用本地函数。
2. **Agent Loop**：通过 `for` 循环实现“思考-行动-观察”的闭环，并设置了最大迭代次数防止死循环。
3. **安全工程**：使用 `python-dotenv` 管理 API 密钥，避免硬编码泄露。
4. **自动化评测**：编写了包含 4 个边界场景的测试集，自动追踪模型的工具调用过程与最终回答，验证了模型拒绝幻觉的能力。

## 运行指南
1. 安装依赖：`pip install openai python-dotenv`
2. 为 `.env`，填入你的 API Key。
3. 运行：`weather.py` 
