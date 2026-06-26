from pathlib import Path

# ============================================================
# PROJECT PATHS — single source of truth
# ============================================================
# Every script imports paths from here instead of hardcoding "data/raw/...".
# To move a folder or rename a file later, change it in THIS file only.
# Rule: only centralize values used in MORE THAN ONE place; single-use
# literals stay where they're used (avoid over-abstraction).

# Project root = the folder this config.py lives in. Resolved to an absolute
# path so paths work no matter which directory a script is run from.
ROOT = Path(__file__).resolve().parent


# ------------------------------------------------------------
# DATA FOLDERS  (where raw source material lives on disk)
# ------------------------------------------------------------
DATA_DIR = ROOT / "data"          # all data lives under here
RAW_DIR = DATA_DIR / "raw"        # untouched source material
BLOG_DIR = RAW_DIR / "blog"       # crawled blog posts (.txt)
API_DIR = RAW_DIR / "api"         # API docs folder


# ------------------------------------------------------------
# NAMED FILES  (specific files referenced from more than one script)
# ------------------------------------------------------------
# api_docs.md: fetch_api_docs writes it, chunk_by_heading reads it — name
# centralized here so both sides always agree.
API_DOCS_FILE = API_DIR / "api_docs.md"


# ------------------------------------------------------------
# CHUNKER OUTPUT  (what the chunking step produces)
# ------------------------------------------------------------
# One JSONL file holding every chunk (blog + api combined), one chunk per line.
CHUNKS_FILE = DATA_DIR / "chunks.jsonl"