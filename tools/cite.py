def cite(sources):
    """
    Formats the sources into a readable citation block.
    sources: list of dicts with 'doc_id', 'chunk_id', 'score'
    """
    if not sources:
        return ""
    
    citations = []
    seen = set()
    
    for s in sources:
        ref = f"[{s['doc_id']}]"
        if ref not in seen:
            citations.append(ref)
            seen.add(ref)
            
    return "Sources: " + ", ".join(citations)
