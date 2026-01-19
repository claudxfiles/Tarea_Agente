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
    
    # 2. PDF Path
    pdf_path = "data/PDF/Ley-21442_13-ABR-2022.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    print(f"Processing PDF: {pdf_path}")
    
    # 3. Extract Text
    full_text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return

    print(f"Extracted {len(full_text)} chars from PDF.")

    # 4. Chunking
    chunks = chunk_text(full_text)
    print(f"Generated {len(chunks)} chunks.")
    
    # 5. Ingest
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk['content'])
        
        if not embedding:
            print(f"Skipping chunk {i} due to embedding error")
            continue
            
        key = f"chunk:ley_copropiedad:{i}"
        
        # Prepare data for Redis
        embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
        
        mapping = {
            "doc_id": "Ley-21442_13-ABR-2022.pdf",
            "chunk_id": chunk['chunk_id'],
            "content": chunk['content'],
            "vector": embedding_bytes
        }
        
        r.hset(key, mapping=mapping)
        if i % 10 == 0:
            print(f"Ingested {i}/{len(chunks)} chunks...")
            
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_documents()
