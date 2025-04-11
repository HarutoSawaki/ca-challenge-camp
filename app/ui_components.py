# app/ui_components.py

import streamlit as st

def render_title():
    st.markdown(
        "<h1 style='color:#ff4b4b; font-weight:bold; text-align:center;'>🔥 渋谷ランチ兄貴チャット 🍱</h1>",
        unsafe_allow_html=True
    )

def render_reference_list(sources):
    st.markdown("📄 <strong>兄貴が参考にした店、ぜんぶ教えるぜ！</strong>", unsafe_allow_html=True)
    for doc in sources:
        name = doc.metadata.get("source", "（店名不明）")
        url = doc.metadata.get("url")
        if url:
            st.markdown(f"- 🍽️ <a href='{url}' target='_blank'><strong>{name}</strong></a>", unsafe_allow_html=True)
        else:
            st.markdown(f"- 🍽️ <strong>{name}</strong>", unsafe_allow_html=True)

def render_footer():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<small style='color:gray;'>© 2024 渋谷ランチ兄貴プロジェクト — powered by LangChain & Streamlit</small>",
        unsafe_allow_html=True
    )
