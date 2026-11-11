import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")


# 1. 定义工具 (和我们之前一样)
def get_weather(city: str) -> str:
    return {"武汉": "晴，25℃", "上海": "多云，27℃"}.get(city, "暂无数据")


tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询城市天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

# 2. 定义我们的测试集 (这就是我们出给 Agent 的考卷)
test_cases = [
    "武汉今天天气怎么样？",  # 正常情况，字典里有
    "北京今天适合出门吗？",  # 挑战 1：字典里没有，看它怎么回答
    "上海和武汉哪个更热？",  # 挑战 2：需要多次调用工具对比
    "今天天气如何？"  # 挑战 3：没有给出城市，看它怎么处理
]

# 3. 开始循环评测
print("开始批量评测...\n" + "=" * 40)

for i, query in enumerate(test_cases):
    print(f"\n测试用例 {i + 1}: {query}")
    messages = [{"role": "user", "content": query}]

    for _ in range(5):
        resp = client.chat.completions.create(
            model="deepseek-chat", messages=messages, tools=tools
        )
        msg = resp.choices[0].message
        messages.append(msg)

        # 【关键】如果模型决定调用工具，我们打印出它的决策
        if msg.tool_calls:
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                print(f"  [过程追踪] 模型决定调用工具，参数: {args}")
                result = get_weather(args["city"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })
        else:
            # 如果模型没有调用工具，直接输出最终回答
            print(f"  [最终回答] {msg.content}")
            break

print("\n" + "=" * 40 + "\n评测结束。")
