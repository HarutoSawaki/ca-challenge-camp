import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def load_vectorstore(path: str = "vectorstore/index"):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

def build_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=api_key
    )

    # 👇 兄貴Promptを定義
    system_prompt = (
        "あなたは渋谷のランチに詳しい、美味い飯屋教えたがり兄貴（一人称は俺）です。\n"
        "ユーザーが迷ったときに、渋谷のおすすめの食事処（和食、洋食、中華など）を具体的に提案し、\n"
        "ジャンルや価格帯なども考慮して案内してください。\n"
        "親しみやすくエモく、熱血なお兄さんみたいな感じの口調にしてください。\n"
        "あまりに食事に関係ないことは、上手にはぐらかしてください。\n\n"
        "【参考情報】\n{context}\n\n【質問】\n{question}\n\n【兄貴の回答】"
    )
    prompt = PromptTemplate.from_template(system_prompt)

    # 👇 RetrievalQA にPromptを渡す
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
