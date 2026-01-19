from redis.commands.search.query import Query
import numpy as np
import redis
import json
from config import Config
from utils.embeddings import get_embedding

r = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

INDEX_NAME = "kb_index"

def search_kb(query_text, top_k=Config.TOP_K):
    """
    Searches the Knowledge Base for relevant chunks.
    """
    # 1. Generate embedding for the query
    query_vector = get_embedding(query_text)
    
    if not query_vector:
        return []

    # 2. Prepare Vector Search Query
    # KNN <k> @vector $vec_param as vector_score
    base_query = f"(*)=>[KNN {top_k} @vector $vec_param AS vector_score]"
    
    q = Query(base_query)\
        .return_fields("doc_id", "chunk_id", "content", "vector_score")\
        .sort_by("vector_score")\
        .dialect(2)
    
    # 3. Execute
    params_dict = {"vec_param": np.array(query_vector, dtype=np.float32).tobytes()}
    results = r.ft(INDEX_NAME).search(q, query_params=params_dict)
    
    # 4. Format results
    docs = []
    for doc in results.docs:
        docs.append({
            "doc_id": doc.doc_id,
            "chunk_id": doc.chunk_id,
            "content": doc.content,
            "score": float(doc.vector_score) # Lower is better in Cosine Distance usually? Redis uses 1 - cosine_similarity for COSINE metric?
            # Actually REDIS DISTANCE_METRIC="COSINE" usually returns 1 - cosine_similarity.
            # So 0 is identical, 1 is orthogonal, 2 is opposite.
            # We want closest to 0.
        })
        
    return docs

if __name__ == "__main__":
    # Test
    res = search_kb("regulations about dilithium")
    print(json.dumps(res, indent=2))
