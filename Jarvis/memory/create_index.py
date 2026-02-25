

from pinecone import Pinecone, ServerlessSpec
import os



pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])



def create_index(index_name=str):
    if index_name not in [i["name"] for i in pc.list_indexes()]:
        print("Creating Index",index_name)
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    else:
        print(f"{index_name} Index already exists")

    return pc.Index(index_name)
    


