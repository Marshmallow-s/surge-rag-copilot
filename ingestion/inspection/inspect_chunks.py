# ingestion/inspection/survey_sources.py
# One-off corpus survey: for each source, print a few sample chunks
# so I can hand-judge what each source is about (golden-set prep, not pipeline).

import json                                          # read jsonl
from collections import defaultdict                  # group chunks by source

from config import CHUNKS_FILE                       # centralized path


# --- 1. Load ---
# Reuse the same load pattern as the retriever: each line is one json chunk.
def load_chunks():
    chunks = []
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


# --- 2. Group by source ---
# Collect all chunks belonging to each source filename into one bucket.
def group_by_source(chunks):
    grouped = defaultdict(list)
    for chunk in chunks:
        grouped[chunk["source"]].append(chunk)
    return grouped


# --- 3. Sample + print ---
# For each source, show how many chunks it has and print the first N,
# truncated, so the terminal stays readable. I read these and write
# one sentence per source describing what it covers.
def survey(grouped, samples_per_source=2, preview_chars=300):
    for source, chunks in grouped.items():
        print("=" * 80)
        print(f"SOURCE: {source}  ({len(chunks)} chunks)")
        print("=" * 80)
        for chunk in chunks[:samples_per_source]:
            print(chunk["text"][:preview_chars].strip())
            print("-" * 40)
        print()


if __name__ == "__main__":
    chunks = load_chunks()
    grouped = group_by_source(chunks)
    survey(grouped)