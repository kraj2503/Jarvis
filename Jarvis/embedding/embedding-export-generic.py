# %%
from openai import OpenAI

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from dotenv import load_dotenv



# %%

load_dotenv("../.env")


# %%

def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents

doc = read_doc('documents/') 

doc 


# %%
# from datasets import load_dataset

# ds = load_dataset("abhinand/MedEmbed-training-triplets-v1", "default")

# %%
# print(ds["train"][0])

# %%
docs = []

for row in ds["train"]:
    docs.append(
        Document(
            page_content=row["pos"],
            metadata={
                "domain": "healthcare",
                "dataset": "MedEmbed",
                "query_hint": row["query"]
            }
        )
    )


# %%
len(docs)


# %%
def chunk_data(docs,chunk_Size=800,chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_Size,chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(docs)
    return docs

chunked_data = chunk_data(docs)

# %%
from langchain_openai import OpenAIEmbeddings

embeddings =OpenAIEmbeddings(model='text-embedding-3-small',api_key=os.environ['OPENAI_API_KEY'])
embeddings

# %% [markdown]
# Large amount of data so going for only 20%

# %%
# texts = [doc.page_content for doc in chunked_data]

# vectors = embeddings.embed_documents(texts)

# print(len(vectors))          # number of chunks
# print(len(vectors[0]))       # embedding dimension (1536)

# %%
sample_size = int(0.04* len(chunked_data))

sampled_docs = chunked_data[:sample_size]
sampled_docs
sample_size

# %%

texts = [doc.page_content for doc in sampled_docs]
vectors = embeddings.embed_documents(texts)

# %%
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import PineconeVectorStore as Pinecone

pc = PineconeClient(api_key=os.environ['PINECONE_API_KEY'])
index_name = 'healthcare'

# %%
print(len(vectors[0]))  

# %%
from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = "healthcare"

if index_name not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)

# %%
import uuid

pinecone_vectors = []

for doc, vector in zip(sampled_docs, vectors):
    pinecone_vectors.append(
        (
            str(uuid.uuid4()),     # unique ID
            vector,                # 1536-dim embedding
            doc.metadata | {
                "text": doc.page_content   # optional but recommended
            }
        )
    )


# %%
BATCH_SIZE = 100

for i in range(0, len(pinecone_vectors), BATCH_SIZE):
    batch = pinecone_vectors[i : i + BATCH_SIZE]
    index.upsert(vectors=batch)

# %%
stats = index.describe_index_stats()
print(stats)

# %%



