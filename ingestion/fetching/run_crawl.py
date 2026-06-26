# import the single-post tool we already built
from fetch_and_save import fetch_and_save

# the list of posts we want to crawl (hand-written for now)
urls = [
    "https://surgehq.ai/blog/handbook-md",
    "https://surgehq.ai/blog/rl-envs-real-world",
    "https://surgehq.ai/blog/how-tiktok-is-evolving-the-next-generation-of-search",
    "https://surgehq.ai/blog/advancedif-and-the-evolution-of-instruction-following-benchmarks",
    "https://surgehq.ai/blog/complexconstraints-a-benchmark-for-entangled-instruction-following",
    "https://surgehq.ai/blog/gdp-pdf-can-100b-ai-models-master-the-documents-that-run-the-world",
    "https://surgehq.ai/blog/hemingway-bench-ai-writing-leaderboard",
    "https://surgehq.ai/blog/lmarena-is-a-plague-on-ai",
    "https://surgehq.ai/blog/finance-eval-real-world",
    "https://surgehq.ai/blog/anthropic-surge-ai-rlhf-platform-train-llm-assistant-human-feedback"
]

# crawl every post in the list
if __name__ == "__main__":
    for url in urls:
        fetch_and_save(url)