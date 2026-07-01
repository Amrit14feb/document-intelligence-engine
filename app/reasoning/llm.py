from langchain_openai import ChatOpenAI

from config import OPENROUTER_API_KEY

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2
)