import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI()

# 1. Define the exact shape I want back
class Answer(BaseModel):
    answer: str
    source_url: str

# 2. Ask the model, forcing the reply into that shape
response = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "What is RLHF? Give a source_url if you have one, else 'none'."}
    ],
    response_format=Answer,
)

# 3. Now I get a real Python object with guaranteed fields
result = response.choices[0].message.parsed
print("ANSWER:", result.answer)
print("SOURCE:", result.source_url)