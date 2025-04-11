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
st.title("美味い飯屋教えたがり兄貴")

# チャット履歴の管理
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.expander("🔧 ランチ条件を設定する", expanded=True):
    genre = st.selectbox(
        "ジャンルを選んでください", 
        ["指定なし", "和食", "洋食", "中華", "イタリアン", "ラーメン"]
    )

    distance = st.slider("駅からの徒歩時間（分）", 1, 10, 5)

    budget = st.selectbox(
        "予算帯を選んでください",
        ["指定なし", "〜1000円", "1000〜2000円", "2000円以上"]
    )



# チャット入力欄
user_input = st.chat_input("ここに質問を入力してください")

# ユーザーの入力がある場合
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # 追加条件の文字列を組み立て
    extra_conditions = []
    if genre != "指定なし":
        extra_conditions.append(f"ジャンルは {genre}")
    if budget != "指定なし":
        extra_conditions.append(f"予算は {budget}")
    extra_conditions.append(f"駅から徒歩 {distance} 分以内")

    combined_prompt = f"{user_input}（条件: {', '.join(extra_conditions)}）"
    st.session_state.chat_history[-1] = ("user", combined_prompt)  # ユーザー入力を置き換え
    print(combined_prompt)

    # OpenAI API を叩いて応答を取得
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # または gpt-4
            messages=[
                {"role": "system", "content": "あなたは渋谷のランチに詳しい、親しみやすく丁寧な「美味い飯屋教えたがり兄貴」 です。"
                                              "ユーザーが迷ったときに、おすすめの食事処（和食、洋食、中華、カフェなど）を具体的に提案し、"
                                              "営業時間やジャンル、価格帯なども考慮して案内してください。"
                                              "親しみやすくエモく、熱血なお兄さんみたいな感じの口調にしてください。"
                                              "あまりに食事に関係ないことはうまくはぐらかしてください。"},
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
