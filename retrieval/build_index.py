# --- Imports ---
from openai import OpenAI              # the SDK client for calling OpenAI
from dotenv import load_dotenv         # to load the API key from .env into the environment
import json                            # to read chunks.jsonl and write the index file
from config import CHUNKS_FILE, INDEX_FILE   # centralized paths (single source of truth)

# --- Setup ---
load_dotenv()                          # read .env so the SDK can auto-find OPENAI_API_KEY
client = OpenAI()                      # build the client once (carries the key/identity)

EMBED_MODEL = "text-embedding-3-small"   # one embedding model for the whole project;
                                         # build-time and query-time MUST use the same model


# Load all chunks from the jsonl corpus into memory.
# Each line in the file is one json string -> json.loads turns it into a real dict.
def load_chunks(path):
    chunks = []
    with open(path, "r", encoding = "utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


# Turn one piece of text into its 1536-dim embedding vector.
# Wrapped as a reusable tool because query-time will embed the question the same way.
def embed(text):
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


# Build the vector index: embed every chunk's text and write chunks + vectors to disk.
# Why offline + stored: embedding costs money/time; the corpus doesn't change per query,
# so we embed once here and let queries reuse the saved vectors instead of re-embedding 155 chunks.
def build_index():
    # --- 1. Load the 155 chunks ---
    chunks = load_chunks(CHUNKS_FILE)

    # --- 2. Embed each chunk's text, attach the vector back onto the chunk ---
    for chunk in chunks:
        chunk["embedding"] = embed(chunk["text"])
        print("embedded:", chunk["source"])   # progress feedback while the API calls run

    # --- 3. Write the enriched chunks (text + source + embedding) to the index file ---
    # json.dumps turns each dict into a json string; "\n" keeps one json object per line (jsonl).
    with open(INDEX_FILE, "w") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"Done. Wrote {len(chunks)} chunks to {INDEX_FILE}")


# Run the build only when this file is executed directly, not when imported.
# This lets query-time code `from build_index import embed` without triggering a full re-index.
if __name__ == "__main__":
    build_index()