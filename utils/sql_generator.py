import re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from utils.extract_schema import get_clean_schema_string

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(schema_text, chunk_size=300):
    """
    Splits schema text into chunks and embeds them into a FAISS index.
    """
    chunks = []
    current_chunk = ""
    
    for line in schema_text.splitlines():
        if len(current_chunk) + len(line) > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = ""
        current_chunk += line + "\n"
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    vectors = model.encode(chunks)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(np.array(vectors))
    return index, vectors, chunks

def generate_sql_prompt(user_prompt):
    """
    Builds a prompt for the LLM by retrieving the most relevant schema chunks.
    """
    schema = get_clean_schema_string()
    index, vectors, chunks = embed_chunks(schema)
    prompt_vec = model.encode([user_prompt])[0]

    D, I = index.search(np.array([prompt_vec]), k=3)
    context = "\n\n".join([chunks[i] for i in I[0]])

    return f"""You are a professional SQL generator.

Using the following database schema context, write a valid MySQL SELECT 
query for the user's request.

### Schema:
{context}

Based on the schema context above, generate a SQL query that answers the 
following user request:
### User Request:
{user_prompt}


    Include necessary JOINs based on the relationships between 
    tables and return all relevant fields. 
    Only return the SQL query, no markdown, no explanations.
### SQL:"""

def clean_sql_query(raw_sql):
    """
    Cleans the AI-generated SQL query by removing markdown or commentary.
    """
    # Remove code block markdown (```sql ... ```)
    cleaned = re.sub(r"```sql|```", "", raw_sql, flags=re.IGNORECASE).strip()

    # Extract actual SELECT statement (safeguard)
    match = re.search(r"(SELECT .*?;)", cleaned, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return cleaned
