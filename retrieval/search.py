import json                          # parse each .jsonl line (a string) into a real dict
from config import CHUNKS_FILE       # absolute path to chunks.jsonl, defined once in config


# --- 1. Index: load all chunks into memory ---
def load_chunks():
    # Collect every chunk dict here; this list IS our in-memory index
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        # Each line in a .jsonl file is one standalone JSON object
        for line in f:
            # A line read from disk is a plain string, even though it looks like a dict;
            # json.loads turns that string into a real dict so we can access ["text"] / ["source"]
            chunks.append(json.loads(line))
    return chunks


# --- 2. Score: how many query words appear in this chunk ---
# Scoring = count how many words from the query also appear in the chunk text.
# More overlap -> higher score -> more likely relevant.
# LIMITATION: this uses substring match (`word in text`), not whole-word match,
# so "use" also matches "used" / "useful", adding some noise. Kept simple on
# purpose for the text-search baseline; revisit when upgrading to vector search.
def score(query, chunk):
    # Lowercase the chunk text so matching ignores case (RLHF == rlhf)
    text = chunk["text"].lower()
    # Lowercase the query the same way, then split into individual words to check one by one
    query_words = query.lower().split()

    # Count how many query words show up anywhere in this chunk
    count = 0
    for word in query_words:
        if word in text:
            count += 1
    return count


# --- 3. Rank: score all chunks, return the top-k most relevant ---
# Ranking = score every chunk, sort by score, keep only the top k.
# This is why retrieval beats dumping all 155 chunks into the LLM: we feed it
# just the few most relevant chunks (cheaper, faster, less diluted signal).
# LIMITATION: ties are broken arbitrarily — when several chunks share the same
# score, their order is undefined, so a "top 3" can be somewhat luck-of-the-draw
# on low-signal queries. Acceptable for the text-search baseline; vector search
# gives finer-grained scores that mostly remove ties.
def rank(query, chunks, k=3):
    # Pair each chunk with its score so we can sort by score but still return the chunk
    scored = []
    for chunk in chunks:
        chunk_score = score(query, chunk)
        scored.append((chunk_score, chunk))

    # Sort by score (the first item of each pair), highest first
    scored.sort(key=lambda pair: pair[0], reverse=True)

    # Drop the scores, return just the top-k chunks
    return [chunk for chunk_score, chunk in scored[:k]]



if __name__ == "__main__":
    chunks = load_chunks()
    results = rank("how is model feedback collected from people", chunks)
    for r in results: 
        print(r["source"])
        print(r["text"][:120])
        print("---")