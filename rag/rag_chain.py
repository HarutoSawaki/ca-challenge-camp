import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


# .envの読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ベクトルストアをロード
def load_vectorstore(path: str = "vectorstore/index"):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# RetrievalQAChain の構築
def build_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=api_key
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": PromptTemplate.from_template(
                "以下の情報をもとに、ユーザーの質問に回答してください。\n"
                "情報:\n{context}\n\n質問: {question}\n\n回答:"
            )
        }
    )


    return qa_chain
