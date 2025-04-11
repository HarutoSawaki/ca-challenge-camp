# rag/test_rag_cli.py

from rag_chain import build_rag_chain

qa = build_rag_chain()

print("🔍 RAGチャット起動！質問を入力してください（終了: q）")
while True:
    query = input("\n🧑 あなた: ")
    if query.lower() in {"q", "quit", "exit"}:
        print("👋 終了します。")
        break

    result = qa(query)
    answer = result["result"]
    sources = result.get("source_documents", [])

    print("\n🤖 回答:")
    print(answer)

    if sources:
        print("\n📄 参照されたドキュメント:")
        for doc in sources:
            print(f"- {doc.metadata['source']}")
