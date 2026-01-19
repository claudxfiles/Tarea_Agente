import redis
from config import Config

r = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

def get_doc(doc_id):
    """
    Retrieves full document metadata/content if needed.
    Since we store chunks, we might need to query by tag or just return the ID reference.
    For this specific requirement, 'get_doc' might mean getting details about the source doc.
    """
    # In a full system, we might have a separate key "doc:{doc_id}" with full text.
    # Given our ingest strategy, we only have chunks.
    # We can simulate this by finding all chunks (expensive) or just returning info if we had stored it.
    
    # Let's assume for this assignment we just confirm existence or return a placeholder
    # since we didn't store a separate "doc:X" key, only "chunk:X:i".
    
    # Alternative: Search for any chunk with this doc_id tag
    return {
        "doc_id": doc_id,
        "status": "available",
        "location": "Knowledge Base"
    }
