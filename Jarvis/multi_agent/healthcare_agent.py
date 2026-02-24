from google.adk.agents  import LlmAgent
from google.adk.tools import google_search
from pinecone import Pinecone as PineconeClient
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# load_dotenv(".env")

import instructions

apikey = ""
print(apikey)

pc = PineconeClient(api_key=apikey)
index_name = 'healthcare'
embeddings = embeddings =OpenAIEmbeddings(model='text-embedding-3-small',api_key="")



def get_similarity_healthcare(query:str, top_k=5,int = 5):
    """
    Get response from internal KB from Pinecone 
    """
    
    
    index = pc.Index("healthcare")
    embedded_query = embeddings.embed_query(query)
    
    res = index.query(
        vector=embedded_query,
        top_k=top_k,
        include_metadata=True
    )
    
    return res


healthcare_agent = LlmAgent(
    name="healthcare_agent",
    static_instruction=instructions.get_instructions("healthcare_agent"),
    
    tools=[google_search]   
)

print(get_similarity_healthcare("Cure of diabetis"))