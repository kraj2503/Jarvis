# rag_tools.py

from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import Tool

vectorstore = Qdrant(
    url="http://localhost:6333",
    collection_name="healthcare_docs",
    embeddings=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

rag_tool = Tool(
    name="medical_knowledge_search",
    description="Search trusted medical knowledge base for healthcare information",
    func=lambda query: retriever.invoke(query)
)