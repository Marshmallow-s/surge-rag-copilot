import requests
from config import API_DIR, API_DOCS_FILE   # centralized folder + file paths

# Surge API docs live as clean markdown in their GitHub repo.
# We pull the raw file directly instead of scraping the live Slate-rendered
# page (which sits behind a login wall and carries navigation noise).
URL = "https://raw.githubusercontent.com/surge-ai/surge-documentation/main/source/index.html.md"


def main():
    # 1. Download. raise_for_status() stops early if the fetch failed
    response = requests.get(URL)
    response.raise_for_status()
    text = response.text  # already markdown — no HTML parsing needed

    # 2. Strip the frontmatter: the "--- ... ---" config block at the very
    #    top is build-tool metadata (title, language_tabs, search), not doc
    #    content. Feeding it to the RAG would just add noise.
    #    split("---", 2) cuts at the FIRST TWO "---" only, giving 3 parts:
    #    ['', '<frontmatter>', '<body>']. We keep [2], the real body.
    body = text.split("---", 2)[2].strip()

    # 3. Save the cleaned body. Create the FOLDER first (API_DIR), then write
    #    the FILE (API_DOCS_FILE). Both come from config so the chunker reads
    #    the exact same path this script writes to.
    API_DIR.mkdir(parents=True, exist_ok=True)
    with open(API_DOCS_FILE, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"Saved API docs -> {API_DOCS_FILE} ({len(body)} chars)")


# Run the fetch only when this file is executed directly, not when imported.
if __name__ == "__main__":
    main()