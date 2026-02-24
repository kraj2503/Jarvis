from pinecone import Pinecone as PineconeClient
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv("Jarvis/.env")


pc = PineconeClient(api_key=os.environ["PINECONE_API_KEY"])
embeddings = embeddings =OpenAIEmbeddings(model='text-embedding-3-small',api_key=os.environ["OPENAI_API_KEY"])



def get_similarity(query:str, index:str,top_k=5):
    """
    Get response from internal Knowledge Base from Pinecone via different Index
    """
    
    
    pinecone_index = pc.Index(index)
    embedded_query = embeddings.embed_query(query)
    
    res = pinecone_index.query(
        vector=embedded_query,
        top_k=top_k,
        include_metadata=True
    )
    
    return res
