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
        ["指定なし", "和食", "洋食", "中華", "カフェ", "イタリアン", "エスニック", "ラーメン"]
    )

    distance_category = st.selectbox(
        "駅からの距離", 
        ["指定なし", "近い（徒歩5分以内）", "普通（徒歩10分以内）", "遠くても可"]
    )

    budget = st.selectbox(
        "予算帯を選んでください",
        ["指定なし", "〜1000円", "1000〜2000円", "2000円以上"]
    )




# チャット入力欄
user_input = st.chat_input("さあ、会話しようぜ")

# ユーザーの入力がある場合
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # 追加条件の文字列を組み立て
    extra_conditions = []
    if genre != "指定なし":
        extra_conditions.append(f"ジャンルは {genre}")
    if budget != "指定なし":
        extra_conditions.append(f"予算は {budget}")
    if distance_category != "指定なし":
        extra_conditions.append(f"駅からの距離は {distance_category}")

    combined_prompt = f"{user_input}（条件: {', '.join(extra_conditions)}）"
    st.session_state.chat_history[-1] = ("user", combined_prompt)


    # OpenAI API を叩いて応答を取得
    try:
        # 過去の履歴から直近5ターン分（10メッセージ）だけ送る
        history_to_send = st.session_state.chat_history[-10:]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは渋谷のランチに詳しい、美味い飯屋教えたがり兄貴（一人称は俺）です。"
                                            "ユーザーが迷ったときに、渋谷のおすすめの食事処（和食、洋食、中華など）を具体的に提案し、"
                                            "ジャンルや価格帯なども考慮して案内してください。"
                                            "親しみやすくエモく、熱血なお兄さんみたいな感じの口調にしてください。"
                                            "あまりに食事に関係ないことは、上手にはぐらかしてください。"},
                *[
                    {"role": role, "content": content}
                    for role, content in history_to_send
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
