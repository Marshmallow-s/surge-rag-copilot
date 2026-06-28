# --- Imports ---
from openai import OpenAI          # the SDK client class
from dotenv import load_dotenv     # to load the API key from .env

# --- Setup ---
load_dotenv()
client = OpenAI()

# --- Probe: embed one piece of text and inspect the raw vector ---
# Why: make "text -> vector" visible before embedding all 155 chunks.
response = client.embeddings.create(model="text-embedding-3-small", input="hello")

vector = response.data[0].embedding    # dig out the actual 1536-number vector

print("length:", len(vector))          # expect 1536
print("first 5:", vector[:5])          # peek at the start, not all 1536