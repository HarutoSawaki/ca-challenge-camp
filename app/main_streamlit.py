import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env から OPENAI_API_KEY を読み込む
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OPENAI_API_KEY が設定されていません。`.env` ファイルを確認してください。")
    st.stop()

# OpenAI クライアント初期化
client = OpenAI(api_key=openai_api_key)

# ページ設定
st.set_page_config(page_title="AI Chat", page_icon="🤖", layout="wide")
st.title("🤖 Chat with AI")

# チャット履歴の管理
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 入力欄
user_input = st.chat_input("ここに質問を入力してください")

# ユーザーの入力がある場合
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # OpenAI API を叩いて応答を取得
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # または gpt-4
            messages=[
                {"role": "system", "content": "あなたは親切なAIアシスタントです。"},
                *[
                    {"role": role, "content": content}
                    for role, content in st.session_state.chat_history
                ]
            ]
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"❌ エラーが発生しました: {e}"

    st.session_state.chat_history.append(("assistant", ai_reply))

# チャット履歴の表示
for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(content)
