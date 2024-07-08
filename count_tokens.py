import os
from dotenv import load_dotenv
import google.generativeai as genai
import datetime
from google.generativeai import caching

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('GEMINI_API_KEY')

# Initialize the generative AI with the API key
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash-001')

# Read content from combined_files.txt
with open('combined_files.txt', 'r') as file:
    content = file.read()

# Count tokens in the content
token_count = model.count_tokens(content)
print(f"Total tokens: {token_count.total_tokens}")
