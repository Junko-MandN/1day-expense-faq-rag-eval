
import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()

# 質問10問を読み込む
questions = json.loads(
    Path("questions.json").read_text(encoding="utf-8")
)

# 規程全文を読み込む
policy = Path("expense_policy.txt").read_text(encoding="utf-8")

total_tokens = 0

for item in questions:
    question = item["question"]

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "あなたは社内経費規程に回答するアシスタントです。"
            "必ず与えられた規程を根拠に回答してください。"
            "規程に記載がない場合は、その旨を明示してください。"
            "推測でルールを補わず、日本語で簡潔に回答してください。"
        ),
        input=(
            f"【社内規程】\n{policy}\n\n"
            f"【質問】\n{question}"
        ),
        max_output_tokens=200,
    )

    print("=" * 50)
    print(f"質問 {item['id']}：{question}")
    print(f"期待する回答：{item['expected_answer']}")
    print(f"AIの回答：{response.output_text}")
    print(f"使用トークン：{response.usage.total_tokens}")

    total_tokens += response.usage.total_tokens

print("=" * 50)
print(f"10問の合計使用トークン：{total_tokens}")
