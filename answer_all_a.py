
import json
from openai import OpenAI

client = OpenAI()

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

total_tokens = 0

for item in questions:
    print("=" * 60)
    print(f"質問{item['id']}: {item['question']}")

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "あなたは社内の経費精算に関する質問に回答するアシスタントです。"
            "会社の規程は与えられていません。一般的な知識だけで断定せず、"
            "会社固有のルールが分からない場合は、その旨を伝えてください。"
        ),
        input=item["question"],
        max_output_tokens=400,
    )

    print("【AIの回答】")
    print(response.output_text)

    usage = response.usage
    print(
        f"【トークン数】入力: {usage.input_tokens}, "
        f"出力: {usage.output_tokens}, "
        f"合計: {usage.total_tokens}"
    )

    total_tokens += usage.total_tokens

print("=" * 60)
print(f"【全10問の合計トークン数】{total_tokens}")
