import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.extract_schema import get_db_schema

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(schema_lines, chunk_size=2):
    # Step 1: Chunk the schema lines
    chunks = []
    for i in range(0, len(schema_lines), chunk_size):
        chunk = "\n".join(schema_lines[i:i + chunk_size])
        chunks.append(chunk)

    # Step 2: Embed the chunks
    embeddings = model.encode(chunks)

    # Step 3: Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, embeddings, chunks
