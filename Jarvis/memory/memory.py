import uuid
import time
from  jarvis.memory.create_index import create_index
from  jarvis.embedding.create_embedding import create_embeddings  

index = create_index("memory")

def write_long_term_vector_memory(
    user_id: str,
    agent: str,
    content: str
) -> str:
    """
    Stores long-term semantic memory as a vector.
    """

    embedding = create_embeddings(content) 
    vectors=[]
    
    for vector in embedding: 
        vectors.append((
            str(uuid.uuid4()),
            vector,
            {
                "user_id":user_id,
                "agent_name":agent,
                "content":content,
                "timestamp":time.time(),
                "memory_type":"long_term_memory",
            }
        ))  
    index.upsert(vectors=vectors)
    return "Memory stored successfully"


def read_long_term_vector_memory(
    user_id: str,
    query: str,
    top_k: int = 5
) -> str:
    """
    Fetch relevant long-term memories for a user.
    """

    query_embedding = create_embeddings(query)[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={
            "user_id": user_id
        }
    )

    if not results or "matches" not in results:
        return ""

    memories = []

    for match in results["matches"]:
        metadata = match.get("metadata", {})
        content = metadata.get("content")
        if content:
            memories.append(content)

    return "\n".join(memories)

