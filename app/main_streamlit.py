import streamlit as st

# ページ設定
st.set_page_config(page_title="RAG Chat", page_icon="🧠", layout="wide")

# ヘッダー
st.title("🧠 Retrieval-Augmented Chatbot")
st.markdown("これはローカルRAG構成で動作するチャットエージェントです。")

# チャット履歴をセッションに保存
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ユーザー入力
user_input = st.chat_input("ここにメッセージを入力...")

# 入力があれば履歴に追加し、応答生成（仮でエコー）
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    
    # ---- 仮の応答部分（ここをLangChainで後ほど置換） ----
    fake_response = f"あなたは「{user_input}」と入力しましたね。これは仮の応答です。"
    st.session_state.chat_history.append(("ai", fake_response))
    # ------------------------------------------------------

# チャット履歴の表示
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("ai"):
            st.markdown(message)
 
#test