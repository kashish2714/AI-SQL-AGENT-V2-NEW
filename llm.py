import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# 1. Load variables from .env file
load_dotenv()

# 2. Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 3. Create LLM object
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0
)