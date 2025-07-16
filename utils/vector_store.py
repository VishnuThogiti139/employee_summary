from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    try:
        if not chunks or not isinstance(chunks, list):
            raise ValueError("Input chunks must be a non-empty list.")

        vectors = []
        for i in range(0, len(chunks), 32):  # Batch size of 32 for large datasets
            batch = chunks[i:i+32]
            vectors.extend(model.encode(batch))

        vectors = np.array(vectors)
        index = faiss.IndexFlatL2(vectors.shape[1])  # Initialize FAISS index
        index.add(vectors)
        return index, vectors, chunks
    
    except Exception as e:
        print(f"Error during embedding: {str(e)}")
        return None, None, None
