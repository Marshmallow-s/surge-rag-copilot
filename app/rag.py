# The RAG orchestrator: retrieve relevant chunks, then ask the LLM to answer
# using ONLY those chunks. This is where R (retrieval) and G (generation) meet.

from retrieval.search import load_chunks, rank   # R: load the index + rank top-k chunks
from app.llm import ask                          # G: send a prompt, get back a structured Answer


# --- 1. Build one big context string out of the retrieved chunks ---
# Each chunk is tagged with its source filename so the model can cite a real
# source instead of inventing a URL (the hallucinated link problem from Step 1).
def build_context(chunks):
    parts = []
    for chunk in chunks:
        # Tag each chunk with its source so the model knows where it came from
        parts.append(f"[source: {chunk['source']}]\n{chunk['text']}")
    # Separate chunks with blank lines so they read as distinct passages
    return "\n\n".join(parts)


# --- 2. The full RAG flow: a question goes in, a grounded Answer comes out ---
def answer_question(question):
    # 1. R: load all chunks, then retrieve the top-3 most relevant to the question
    chunks = load_chunks()
    top_chunks = rank(question, chunks, k=3)

    # 2. Stitch those chunks into a single labelled context block
    context = build_context(top_chunks)

    # 3. The grounding prompt — the heart of RAG. These instructions force the
    #    model to answer ONLY from the retrieved context and to cite the real
    #    source filename, which is what makes the answer traceable and checkable.
    prompt = f"""
            You are a retrieval assistant for Surge AI's documents. 
            Answer the question using only the context below; do not use your own knowledge. 
            If the context does not contain the answer, say "The provided documents don't cover this." Do not guess. 
            For source_url, copy the exact filename shown in [source:...]. Never make up a url. 

            context: {context}
            question: {question}
    """
    # 4. G: send the grounding prompt to the LLM, get back {answer, source_url}
    return ask(prompt)


# --- 3. Runs only when executed directly: a quick end-to-end RAG self-test ---
if __name__ == "__main__":
    result = answer_question("How does Anthropic use RLHF?")
    print("ANSWER:", result.answer)
    print("SOURCE:", result.source_url)