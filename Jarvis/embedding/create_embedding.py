from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
load_dotenv("Jarvis/.env")



embeddings =OpenAIEmbeddings(model='text-embedding-3-small',api_key=os.environ['OPENAI_API_KEY'])


def chunk_data(text:str,chunk_Size=800,chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_Size,chunk_overlap=chunk_overlap)
    text = splitter.split_text(text)
    return text




def create_embeddings(content:str)->  list[list[float]]:

    if len(content)>200:
        content = chunk_data(content)
        
    vectors = embeddings.embed_documents(content)
    return vectors



