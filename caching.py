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

# Create the cached content with only the system instruction
system_instruction = """hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi soy sauce
""" * 1600

# Create the context cache with the system instruction
cached_content = caching.CachedContent.create(
    # model="gemini-1.5-pro-001",
    model="gemini-1.5-flash-001",
    system_instruction=system_instruction,
    ttl=datetime.timedelta(minutes=5),
)

# Use the cached content to create a model
model = genai.GenerativeModel.from_cached_content(cached_content=cached_content)

# Start a chat session
chat_session = model.start_chat(
    history=[]
)

response = chat_session.send_message("the first message says hi hi... then what? what's the last word after that?")

print(response.text)

# for c in caching.CachedContent.list():
#   print(c)