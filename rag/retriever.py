import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from rag.data_loader import load_lunch_csv

def create_vectorstore(save_path: str = "vectorstore/index"):
    load_dotenv()  # ← .envからAPIキー読み込み
    api_key = os.getenv("OPENAI_API_KEY")

    print("📦 ドキュメント読み込み中...")
    documents = load_lunch_csv()

    print("🧠 OpenAI埋め込みモデルを初期化...")
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    print("📈 ベクトルストアを構築中...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    print(f"💾 保存中... {save_path}")
    os.makedirs(save_path, exist_ok=True)
    vectorstore.save_local(save_path)

    print("✅ ベクトルストアの保存完了！")
