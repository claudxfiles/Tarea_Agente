import os
import redis
import pypdf
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
VECTOR_DIM = 1536 

def create_index():
    try:
        # Check if index exists
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
    # 1. Clear Redis
    print("Clearing Redis database...")
    r.flushall()
    create_index() # Re-create index after flush
    
    # 2. Source Directory
    docs_dir = "data/Doc_2"
    if not os.path.exists(docs_dir):
        print(f"Error: Directory not found at {docs_dir}")
        return

    # 3. Get all .txt files
    files = [f for f in os.listdir(docs_dir) if f.endswith('.txt')]
    print(f"Found {len(files)} text files in {docs_dir}")
    
    total_chunks_ingested = 0
    
    for filename in files:
        file_path = os.path.join(docs_dir, filename)
        print(f"Processing file: {filename}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        print(f"Read {len(content)} chars from {filename}.")

        # 4. Chunking
        chunks = chunk_text(content)
        print(f"Generated {len(chunks)} chunks for {filename}.")
        
        # 5. Ingest
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk['content'])
            
            if not embedding:
                print(f"Skipping chunk {i} of {filename} due to embedding error")
                continue
                
            # Create a unique key using filename and chunk index
            key = f"chunk:{filename}:{i}"
            
            # Prepare data for Redis
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            
            mapping = {
                "doc_id": filename,
                "chunk_id": chunk['chunk_id'],
                "content": chunk['content'],
                "vector": embedding_bytes
            }
            
            r.hset(key, mapping=mapping)
            total_chunks_ingested += 1
            
        print(f"Ingested {len(chunks)} chunks from {filename}.")
            
    print(f"Ingestion complete. Total chunks ingested: {total_chunks_ingested}")


if __name__ == "__main__":
    ingest_documents()
