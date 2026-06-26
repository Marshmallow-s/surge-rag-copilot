from config import API_DOCS_FILE   # centralized path to data/raw/api/api_docs.md


def chunk_by_heading(text):
    # API docs split on "## " endpoint headings, NOT blank lines: each endpoint
    # (its definition, code samples, response, params) stays whole in one chunk.
    # We use "## " (two hashes), not "# ", because code blocks contain comments
    # like "# For POST requests" — splitting on "# " would cut inside code.
    lines = text.split("\n")

    chunks = []
    current = []   # lines of the chunk currently being built

    for line in lines:
        # A new "## " heading means the previous endpoint just ended. Close it
        # off — but only if current already has content, so the intro text
        # before the first heading doesn't get saved as an empty chunk.
        if line.startswith("## ") and current:
            chunks.append("\n".join(current))   # glue this endpoint's lines into one chunk
            current = []                         # start fresh for the new endpoint

        # Every line (including the heading itself) goes into the current chunk
        current.append(line)

    # After the loop, the last endpoint is still in current — save it
    if current:
        chunks.append("\n".join(current))

    return chunks


# Standalone test: run this file directly to sanity-check the heading split on
# the real API docs. Guarded by __main__ so it does NOT run when this function
# is imported by chunk_all.py later.
if __name__ == "__main__":
    # Read the API docs file (path comes from config, not hardcoded)
    with open(API_DOCS_FILE, "r", encoding="utf-8") as f:
        body = f.read()

    # Chunk it and capture the returned list
    chunks = chunk_by_heading(body)

    # Print one line per chunk: its index, length, and first line (should be a
    # "## " heading) — quick way to verify each endpoint stayed whole
    print(f"Total: {len(chunks)} chunks\n")
    for i, c in enumerate(chunks):
        first_line = c.split("\n")[0]
        print(f"CHUNK {i} (len {len(c)}): {first_line!r}")