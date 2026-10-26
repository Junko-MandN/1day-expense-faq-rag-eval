
import csv

question_id = input("確認したい質問番号を入力してください（1〜10）: ").strip()

with open("results.csv", "r", encoding="utf-8-sig", newline="") as f:
    rows = csv.DictReader(f)

    for row in rows:
        if row["question_id"] == question_id:
            print("=" * 50)
            print("方式:", row["method"])
            print("質問:", row["question"])
            print("回答:", row["answer"])
            print("トークン数:", row["total_tokens"])
