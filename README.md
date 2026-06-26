# Surge AI RAG Q&A

A retrieval-augmented generation (RAG) question-answering system built on Surge AI's
documentation and technical blog — ask in natural language, get answers grounded in
real source documents, with citations back to where each answer came from.

> 🚧 **Status: in progress.** Building in the open, step by step. See [Progress](#progress) below.

## Why this exists

A lot of knowledge work means hunting through hundreds of long documents — handbooks,
playbooks, slide decks — to answer one specific question. In my consulting work, the only
tool was keyword search: you guess the right term, scan dozens of files by hand, and still
risk missing the one passage that mattered. You can't just ask the question in plain English.

This project builds the thing that would have helped: a system you query in natural language,
that retrieves the relevant passages across a large messy corpus, and answers with a citation
back to the source — so you can trust it and verify it. I'm using Surge AI's technical content
as the corpus because it's a dense, real, vertical domain (RLHF, red-teaming, evaluation
methodology) that general models get wrong and can't cite.

## Progress

- [x] **Step 1 — LLM API + structured output** — calls OpenAI, returns `{answer, source_url}`
- [ ] **Step 2 — Ingestion** — 🚧 crawl + clean done (11 posts in `data/raw/`); chunking next
- [ ] **Step 3 — Retrieval** — search + answer generation
- [ ] **Step 4 — Evaluation** — golden set + LLM-as-judge scorecard
- [ ] **Step 5–6 — Tests / CI / deploy** — demo link + monitoring

## Setup