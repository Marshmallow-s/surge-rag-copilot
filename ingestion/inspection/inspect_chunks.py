import json
from collections import Counter
from config import CHUNKS_FILE   # the chunker's combined output (blog + api)

# Load every chunk back from the JSONL file, one JSON object per line
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]

print(f"Total chunks: {len(chunks)}\n")

# Look at the first few chunks to spot-check chunk quality: does a chunk start
# mid-word/mid-sentence (a bad blind cut) or on a clean boundary?
for i in range(3):
    c = chunks[i]
    print(f"===== CHUNK {i}  (source: {c['source']}, len: {len(c['text'])}) =====")
    print(repr(c["text"][:80]))   # show the start: clean opening, or half a word?
    print("...")
    print(repr(c["text"][-80:]))  # show the end: clean close, or cut off mid-sentence?
    print()

# Count chunks per source file — confirms every file made it in, and shows the
# blog/api split at a glance (catches a missing folder or wrong path)
counts = Counter(c["source"] for c in chunks)
print("Chunks per source:")
for source, n in sorted(counts.items()):
    print(f"  {n:3}  {source}")
print(f"\nDistinct source files: {len(counts)}")