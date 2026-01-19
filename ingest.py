import os
import redis
from redis.commands.search.field import TextField, VectorField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import numpy as np
from config import Config
from utils.chunking import chunk_text
from utils.embeddings import get_embedding

# Setup Redis
r = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

INDEX_NAME = "kb_index"
VECTOR_DIM = 1536 # OpenAI text-embedding-3-small dim

def create_index():
    try:
        r.ft(INDEX_NAME).info()
        print("Index already exists.")
    except Exception:
        print("Creating index...")
        schema = (
            TagField("doc_id"),
            TagField("chunk_id"),
            TextField("content"),
            VectorField("vector",
                "FLAT", {
                    "TYPE": "FLOAT32",
                    "DIM": VECTOR_DIM,
                    "DISTANCE_METRIC": "COSINE"
                }
            )
        )
        r.ft(INDEX_NAME).create_index(
            schema,
            definition=IndexDefinition(prefix=["chunk:"], index_type=IndexType.HASH)
        )
        print("Index created.")

def ingest_documents():
    data_dir = "data/documents"
    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    
    print(f"Found {len(files)} documents.")
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            
        chunks = chunk_text(text)
        print(f"Processing {filename}: {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            # Extract basic metadata from first few lines if possible, or just use filename
            # For simplicity, we use filename
            embedding = get_embedding(chunk['content'])
            
            if not embedding:
                print(f"Skipping chunk {i} due to embedding error")
                continue
                
            key = f"chunk:{filename}:{i}"
            
            # Prepare data for Redis
            # redis-py requires bytes for vector field
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            
            mapping = {
                "doc_id": filename,
                "chunk_id": chunk['chunk_id'],
                "content": chunk['content'],
                "vector": embedding_bytes
            }
            
            # Using HSET for Hash
            r.hset(key, mapping=mapping)
            
    print("Ingestion complete.")

if __name__ == "__main__":
    create_index()
    ingest_documents()
