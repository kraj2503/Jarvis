
from Jarvis.memory.memory import read_long_term_vector_memory, write_long_term_vector_memory


def read_memory(user_id,query,top_k=10):
    """
    Tool to call read memory function
    """
    
    
    return read_long_term_vector_memory(user_id,query,top_k)
    
    


def write_memory( user_id: str, agent: str, content: str):
    """
    Tool to call write memory function
    """
    
    return write_long_term_vector_memory(user_id,agent,content)