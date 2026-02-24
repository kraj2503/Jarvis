from openai import OpenAI

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



client = OpenAI()


def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents

doc = read_doc('documents/') 

def chunk_data(docs,chunk_Size=800,chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_Size,chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(docs)
    return docs

chunk_data(doc)
len(doc)


response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
)

print(response.data[0].embedding)