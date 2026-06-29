# vector_search.py — the retriever (vector version): index / score / rank.
# Same three-layer skeleton as text_search.py, but "relevance" is now measured by
# meaning (vector closeness) instead of literal word overlap. Kept as a SEPARATE
# file from text_search.py so both versions stay runnable side by side for the
# before/after comparison.

import json                              # parse each .jsonl line (a string) into a real dict
import numpy as np                       # vector math: dot product and vector length (norm)
from config import INDEX_FILE            # absolute path to index.jsonl (chunks WITH embeddings)
from retrieval.build_index import embed  # reuse the SAME embed tool so query & chunks share one model


# --- 1. Index: load all chunks (now WITH embeddings) into memory ---
# Reads INDEX_FILE instead of the raw chunks file: every chunk now also carries
# chunk["embedding"] (a 1536-number vector built offline by build_index.py).
def load_chunks():
    chunks = []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        # Each line is one standalone JSON object; json.loads turns the string into a dict
        for line in f:
            chunks.append(json.loads(line))
    return chunks


# --- helper: cosine similarity between two vectors ---
# Cosine similarity = the cosine of the angle between two vectors.
# ~1 = same direction (very similar meaning), 0 = unrelated, -1 = opposite.
# Higher = more similar. Dividing by the two lengths (norms) cancels out vector
# magnitude, so we compare direction (meaning) only, not text length.
def cosine_similarity(a, b):
    # Convert the incoming lists into numpy arrays so we can do vector math on them
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# --- 2. Score: how similar is this chunk's vector to the query's vector ---
# No longer counts word overlap (that was text_search). Compares MEANING via
# vector closeness. Takes the already-embedded query vector (embedded once in
# rank, not here) so we don't re-embed the same query for every chunk.
def score(query_vector, chunk):
    return cosine_similarity(query_vector, chunk["embedding"])


# --- 3. Rank: score all chunks, return the top-k most relevant ---
# Same skeleton as text_search: score every chunk, sort, keep top k.
# Still reverse=True because higher cosine = more similar (a distance metric
# would flip this; cosine similarity does not).
def rank(query, chunks, k=3):
    # Embed the query ONCE, outside the loop. Inside the loop it would re-embed the
    # same query 155 times — one wasted API call per chunk (slow + costs money).
    query_vector = embed(query)

    # Pair each chunk with its similarity score so we can sort by score but still return the chunk
    scored = []
    for chunk in chunks:
        chunk_score = score(query_vector, chunk)
        scored.append((chunk_score, chunk))

    # Sort by the score (position 0 of each pair), highest first
    scored.sort(key=lambda pair: pair[0], reverse=True)

    # Drop the scores, return just the top-k chunks
    return [chunk for (chunk_score, chunk) in scored[:k]]


# Run a quick retrieval test only when executed directly, not when imported.
if __name__ == "__main__":
    chunks = load_chunks()
    results = rank("Why do the rules for tagging data stop working over time?", chunks)
    for r in results:
        print(r["source"])
        print(r["text"])
        #print(r["text"][:120])
        print("---")