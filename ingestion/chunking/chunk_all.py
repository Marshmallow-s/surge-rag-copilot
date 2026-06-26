import json  # serialize each chunk dict into a JSON line
from config import BLOG_DIR, API_DOCS_FILE, CHUNKS_FILE
from ingestion.chunking.chunk_by_heading import chunk_by_heading


# Split a document into chunks that end on paragraph boundaries (blank lines),
# never mid-word or mid-sentence. We pack whole paragraphs into a chunk until
# adding the next one would exceed chunk_size, then start a fresh chunk.
def chunk_by_paragraph(text, chunk_size=800):
    # Split the document into paragraphs on blank lines
    paragraphs = text.split("\n\n")

    chunks = []       # finished chunks
    current = ""      # the chunk currently being filled

    for para in paragraphs:
        # If adding this paragraph would push the current chunk over the limit,
        # close off the current chunk and start a new one with this paragraph
        if len(para) + len(current) > chunk_size:
            chunks.append(current)
            current = para
        else:
            # Otherwise append this paragraph; re-insert the "\n\n" separator,
            # but skip it for the very first paragraph so chunks don't start
            # with stray blank lines
            current = current + "\n\n" + para if current else para
    # After the loop, the last in-progress chunk still needs to be saved
    if current:
        chunks.append(current)
    return chunks


'''
# --- KEPT FOR COMPARISON, NOT USED ---
# Original first-pass chunker: blind fixed-width cut with overlap. Replaced by
# chunk_by_paragraph because this version splits mid-word and mid-sentence.
def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        chunks.append(text[start:end])
        start = start + chunk_size - overlap
    return chunks
'''


# Collect chunks from all sources into one list
all_chunks = []

# 1. Blog posts: each file in BLOG_DIR is prose, so split on paragraphs.
#    iterdir() yields the full path to each file; path.name is just the filename.
for path in BLOG_DIR.iterdir():
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    # Tag every chunk with its source file so results stay traceable later
    for piece in chunk_by_paragraph(text):
        all_chunks.append({"text": piece, "source": path.name})

# 2. API docs: a single structured file, so split on "## " endpoint headings
#    instead of paragraphs (keeps each endpoint whole).
with open(API_DOCS_FILE, "r", encoding="utf-8") as file:
    text = file.read()
for piece in chunk_by_heading(text):
    all_chunks.append({"text": piece, "source": API_DOCS_FILE.name})

# Write all chunks to one JSONL file: one JSON object per line, so the next
# step (indexing) can read them back one chunk at a time
with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
    for chunk in all_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

print(f"Wrote {len(all_chunks)} chunks -> {CHUNKS_FILE}")