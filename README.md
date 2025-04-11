# ca-challenge-camp
CA研修_個人開発ワーク250411


# 渋谷ランチ兄貴チャット 🍱🔥

**「渋谷でランチ迷ったら、とりあえず兄貴に聞け！」**

本アプリは、渋谷周辺の飲食店情報をもとに、OpenAIのChatGPTとLangChainを組み合わせて構築したRAG型チャットアプリです。  
熱血でエモい「兄貴」が、おすすめのランチスポットを提案してくれます。

---

## 🚀 機能概要

- 渋谷ランチに特化した RAG (Retrieval-Augmented Generation)
- FAISS によるローカルベクトル検索
- Streamlit ベースのチャットUI（兄貴キャラ搭載）
- 食べログURLなどのメタ情報もあわせて提示

---

## 📁 ディレクトリ構成

```
ca_challenge-camp/
├── app/
│   ├── main_streamlit.py       ← Streamlitアプリ本体
│   └── ui_components.py        ← UI部品の共通化
├── rag/
│   ├── data_loader.py          ← CSVをDocument形式に変換
│   ├── retriever.py            ← ベクトルDB作成（FAISS）
│   └── rag_chain.py            ← LangChainのRAG構築
├── data/documents/
│   └── 渋谷ランチ.csv          ← 店舗データ（タブ区切り）
├── vectorstore/
│   └── index/                  ← 保存済みベクトルデータ
├── .streamlit/config.toml      ← カスタムテーマ設定
└── README.md
```

---

## 🛠 セットアップ手順

1. 仮想環境を構築：

```bash
conda env create -f environment.yml
conda activate challenge-camp
```

2. `.env` ファイルを作成：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

3. ランチ情報をベクトル化（初回またはCSV更新時に実行）：

```bash
python -c "from rag.retriever import create_vectorstore; create_vectorstore()"
```

4. アプリ起動：

```bash
streamlit run app/main_streamlit.py
```

---

## 🍛 CSVデータの形式と追加手順

`data/documents/渋谷ランチ.csv` は以下のような **タブ区切りファイル** です：

| 店名 | ジャンル | 食べログ | 徒歩距離 | コメント |
|------|----------|----------|----------|----------|
| トンカツ ツキウマ 神山町店 | とんかつ | https://... | 中(3~8分程度) | うまい、けど胃にくる |

### ✅ データを追加するには：

1. `渋谷ランチ.csv` にレコードを追記する  
2. ベクトルストアを再構築する：

```bash
python -c "from rag.retriever import create_vectorstore; create_vectorstore()"
```

> ※再実行により、ベクトルDB `vectorstore/index/` が上書きされます

---

## 💬 開発メモ

- UIパーツは `app/ui_components.py` に集約されています
- `PromptTemplate` により、兄貴キャラの口調を維持した回答が生成されます
- ベクトル検索には FAISS（Facebook製ライブラリ）を使用
- LangChain v0.2 対応済（`langchain_community` モジュール使用）

---

## 🤝 今後の展望

- 画像付きカードUI（店舗外観表示など）
- フィルターによる事前絞り込み（ジャンル・価格・距離）
- 会話ログの保存機能
- モバイル向けデザイン

---

## 📜 ライセンス

本プロジェクトは個人利用・学術目的に限り自由に使用可能です。  
商用利用を希望する場合は事前にご相談ください。

---

🍽️ **兄貴と一緒に、最高の渋谷ランチを探そう！**
