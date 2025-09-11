from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Still using ChatOpenAI but configured for OpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

# Configure for OpenRouter instead of OpenAI
model = ChatOpenAI(
    model="meta-llama/llama-3-70b-instruct",  # Example model (choose any from OpenRouter)
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),  # Your OpenRouter API key
)

parser = StrOutputParser()

# Chain remains the same: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({"question": "What is the capital of Peru?"})
print(result)