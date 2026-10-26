
import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()

questions = json.loads(
    Path("questions.json").read_text(encoding="utf-8")
)
policy = Path("expense_policy.txt").read_text(encoding="utf-8")

total_tokens = 0

for item in questions:
    question = item["question"]

    # 質問文の言葉を、規程で使われる言葉にも対応させる
    keyword_groups = {
        "ホテル": ["ホテル", "宿泊費"],
        "宿泊費": ["ホテル", "宿泊費"],
        "締め日": ["締め日", "支払い"],
        "証憑": ["証憑", "支払い"],
        "領収書": ["領収書", "証憑"],
    }

    base_keywords = [
        "一般社員", "管理職", "取締役", "グリーン車",
        "飛行機", "ビジネスクラス", "宿泊費", "ホテル",
        "領収書", "証憑", "タクシー", "精算",
        "締め日", "支払い", "食事代", "出張"
    ]

    keywords = [
        word for word in base_keywords
        if word in question
    ]

    # 質問に含まれる語に関連する規程用語も検索に加える
    expanded_keywords = set(keywords)

    for word in keywords:
        expanded_keywords.update(keyword_groups.get(word, []))

    keywords = list(expanded_keywords)
 


    lines = policy.splitlines()
    matched_lines = [
        line for line in lines
        if any(keyword in line for keyword in keywords)
    ]

    retrieved_policy = "\n".join(matched_lines)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "あなたは社内経費規程に回答するアシスタントです。"
            "必ず与えられた検索結果を根拠に回答してください。"
            "検索結果に答えがない場合は、記載がないと明示してください。"
            "推測でルールを補わず、日本語で簡潔に回答してください。"
        ),
        input=(
            f"【検索で見つかった規程】\n{retrieved_policy}\n\n"
            f"【質問】\n{question}"
        ),
        max_output_tokens=200,
    )

    print("=" * 50)
    print(f"質問 {item['id']}：{question}")
    print(f"検索キーワード：{keywords}")
    print(f"検索された規程行数：{len(matched_lines)}")
    print(f"期待する回答：{item['expected_answer']}")
    print(f"AIの回答：{response.output_text}")
    print(f"使用トークン：{response.usage.total_tokens}")

    total_tokens += response.usage.total_tokens

print("=" * 50)
print(f"10問の合計使用トークン：{total_tokens}")
