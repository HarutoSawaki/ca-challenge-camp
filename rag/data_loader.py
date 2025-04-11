import pandas as pd
from langchain.schema import Document

def load_lunch_csv(path: str = "data/documents/渋谷ランチ.csv") -> list[Document]:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()  # 念のため空白除去

    print("📌 読み込んだカラム一覧:", df.columns.tolist())  # ← カラム名チェック

    documents = []
    for i, (_, row) in enumerate(df.iterrows()):
        try:
            content = (
                f"店名: {row['店名']}\n"
                f"ジャンル: {row['ジャンル']}\n"
                f"徒歩距離: {row['徒歩距離']}\n"
                f"コメント: {row['コメント']}"
            )
        except KeyError as e:
            print(f"❌ KeyError: {e} — 該当行で処理をスキップします")
            continue

        documents.append(Document(
            page_content=content,
            metadata={
                "source": row["店名"],
                "url": row["食べログ"]
            }
        ))
    
    return documents
