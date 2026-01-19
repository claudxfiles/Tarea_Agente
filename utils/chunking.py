import hashlib

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of `chunk_size` characters with `overlap`.
    Returns a list of dicts with text and metadata.
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk_content = text[start:end]
        
        # Adjust end to avoid splitting words if possible? 
        # For simplicity, we'll strict cut or find nearest space
        # (Optional improvement: finding last space)
        
        chunk_id = hashlib.md5(chunk_content.encode('utf-8')).hexdigest()
        
        chunks.append({
            "chunk_id": chunk_id,
            "content": chunk_content,
            "start": start,
            "end": end
        })
        
        start += (chunk_size - overlap)
    
    return chunks
