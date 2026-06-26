from dotenv import load_dotenv         # load OPENAI_API_KEY from .env into the environment
from openai import OpenAI              # official OpenAI SDK
from pydantic import BaseModel         # declare the exact shape of the model's reply

load_dotenv()                          # read .env and push OPENAI_API_KEY into the environment
client = OpenAI()                      # create the API client; it auto-reads OPENAI_API_KEY from the environment


# --- 1. The fixed shape we force every reply into (structured output) ---
# Pydantic model = a contract for the reply: the model MUST return these two
# fields, cleanly separated. This separation is what makes answers traceable
# (show the source) and auto-gradable later in eval (faithfulness scoring).
class Answer(BaseModel):
    answer: str                       
    source_url: str                    


# --- 2. Reusable tool: send any prompt, get back a structured Answer ---
# Wrapped in a function so any caller (e.g. the RAG flow) can reuse it with any
# prompt — not a one-off script. 
def ask(prompt):
    # .parse() (not .create()) is the structured-output call: response_format
    # constrains decoding so the reply is guaranteed to match the Answer schema
    response = client.chat.completions.parse(
        model = "gpt-4o-mini",        
        messages = [
            {"role": "user", "content": prompt}   
        ],
        response_format = Answer,      
    )
    # The raw response is an envelope; the parsed Answer object lives here.
    return response.choices[0].message.parsed


if __name__ == "__main__":
    result = ask("What is RLHF? Give a source_url if you have one, else 'none'.")
    print("ANSWER: ", result.answer)
    print("SOURCE: ", result.source_url)