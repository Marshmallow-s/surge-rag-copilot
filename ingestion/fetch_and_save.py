import requests                  # library for fetching web pages over HTTP
from bs4 import BeautifulSoup    # library for parsing messy HTML into a navigable structure
import os                        # standard library for file/folder operations

# known site-wide footer lines to drop (verified across 4+ posts)
FOOTER_NOISE = {
    "Smart ≠ Useful",
    "Raise AGI with the richness of human intelligence.",
}

# fetch a single blog post, clean it down to body text, and save it to disk
def fetch_and_save(url):
    # ----------- 1. Fetch --------------------------------------
    # send a GET request and store the full response
    resp = requests.get(url)

    # use the last segment of the url as the filename (e.g. "handbook-md")
    slug = url.split("/")[-1]

    # ----------- 2. Clean --------------------------------------
    # parse the raw HTML so we can pick out content by tag
    soup = BeautifulSoup(resp.text, "html.parser")

    # collect the pieces we keep, in document order
    parts = []

    # grab every h2, h3, and p tag (our cleaning rule), in page order
    for tag in soup.find_all(["h2", "h3", "p"]):
        # pull out the tag's text; strip() trims surrounding whitespace
        text = tag.get_text().strip()
        # skip empty tags, keep the rest
        if text and text not in FOOTER_NOISE:
            parts.append(text)

    # join the kept pieces with a blank line between them into one document
    clean_text = "\n\n".join(parts)

    # ----------- 3. Write --------------------------------------
    # ensure the output folder exists before writing (no error if it already does)
    os.makedirs("data/raw", exist_ok=True)

    # write cleaned text to disk so we don't have to re-fetch every time
    # "w" overwrites if the file exists; utf-8 handles special chars like τ, §, ≠
    with open(f"data/raw/{slug}.txt", "w", encoding="utf-8") as f:
        f.write(clean_text)


# only runs when this file is executed directly, not when imported elsewhere
if __name__ == "__main__":
    # quick self-test on a single post
    url = "https://surgehq.ai/blog/how-tiktok-is-evolving-the-next-generation-of-search"
    fetch_and_save(url)