
import os

from pathlib import Path
from functools import lru_cache
from operator import itemgetter

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
groq_api_key = os.environ["GROQ_API_KEY"]
google_api_key = os.environ["GOOGLE_API_KEY"]

class RAGService:

    def __init__(self):

        print("Initializing RAG service...")

        # 1. Initialize embedding model (ONCE)
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

        # 2. Initialize vector database (ONCE)
        self.vectordb = Chroma(
            persist_directory=str(BASE_DIR / "docs" / "chroma"),
            embedding_function=self.embedding
        )

        # 3. Initialize retriever (ONCE)
        self.retriever = self.vectordb.as_retriever(
            search_kwargs={"k": 3}
        )

        # 4. Initialize LLM (ONCE)
        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-3.8-flash",
        #     google_api_key=google_api_key,
        #     temperature=0
        # )
        self.llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0,
            api_key=groq_api_key
        )
        # 5. Create prompt
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are a helpful document assistant.

                Answer using only the provided context.
                If the answer is not available in the context,
                say you don't know.

                Context:
                {context}
                """
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

        # 6. Create RAG chain (ONCE)
        self.rag_chain = (
            {
                "context": itemgetter("question")
                    | self.retriever
                    | self.format_docs,

                "question": itemgetter("question"),

                "chat_history": itemgetter("chat_history")
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        print("RAG service initialized successfully!")

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(
            doc.page_content for doc in docs
        )

    def ask(self, question, chat_history=None):

        if chat_history is None:
            chat_history = []

        answer = self.rag_chain.invoke({
            "question": question,
            "chat_history": chat_history
        })

        return answer


# Create a singleton instance (lazy initialization)
@lru_cache(maxsize=1)
def get_rag_service():
    return RAGService()
ans=get_rag_service().ask("tell me about Remote pilot license training.")
print(ans)
# from langchain_chroma import Chroma
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from huggingface_hub import login
# from langchain_classic.memory import ConversationBufferMemory
# from langchain_groq import ChatGroq

# from langchain_ollama import ChatOllama



# import os
# import sys
# persist_directory= 'docs/chroma/'
# CHAT_MODEL = "qwen3:8b"

# sys.path.append('../..')

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv())
# google_api_key = os.environ["GOOGLE_API_KEY"]
# hf_token = os.environ["HF_TOKEN"]
# groq_api_key = os.environ["GROQ_API_KEY"]


# login(token=hf_token)
# def rag_service(question):
#     embedding = HuggingFaceEmbeddings(
#             model_name="sentence-transformers/all-MiniLM-L6-v2",
#             model_kwargs={"device": "cpu"},
#             encode_kwargs={"normalize_embeddings": True}
            
#         )

#     vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
#     # llm = ChatOllama(
#     #         model=CHAT_MODEL,
#     #         temperature=0,
#     #         num_predict=100,
#     #         num_ctx=4096,
#     #         reasoning=False
#     #     )
#     # llm = ChatGoogleGenerativeAI(
#     #         model="gemini-3.8-flash",
#     #         google_api_key=google_api_key,
#     #         temperature=0
#     #     )
    
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         return_messages=True
#     )
#     llm = ChatGroq(
#         model="openai/gpt-oss-120b",
#         temperature=0,
#         api_key=groq_api_key
#     )
#     retriever = vectordb.as_retriever(
#         search_kwargs={"k": 3}
#     )
        
#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)

#     prompt = ChatPromptTemplate.from_template("""
#     Answer the question based only on the following context.

#     If you cannot find the answer, say you don't know.

#     Context:
#     {context}

#     Question:
#     {question}
#     """)

#     rag_chain = (
#         {
#             "context": retriever | format_docs,
#             "question": RunnablePassthrough()
#         }
#         | prompt
#         | llm
#         |memory
#         | StrOutputParser()
#     )
#     return rag_chain.invoke(question)

# question = "tell me about Remote pilot license training."

# answer = rag_service(question)
# print(answer)