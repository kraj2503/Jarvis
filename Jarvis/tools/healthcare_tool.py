
from Jarvis.tools.RAG_tools.semantic_search import get_similarity


def get_healthcare_similarity(query:str):
    index = "healthcare"
    res = get_similarity(query,index);
    
    return {
        "matches": [
            {
                "id": match["id"],
                "score": float(match["score"]),  # force Python float
                "text": match["metadata"].get("text", ""),
                "metadata": {
                    k: v for k, v in match["metadata"].items()
                    if isinstance(v, (str, int, float, bool))
                }
            }
            for match in res["matches"]
        ]
    }