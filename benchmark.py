import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
import datetime
from google.generativeai import caching

# Load environment variables from .env file
load_dotenv()

model="gemini-1.5-flash-001"
# model="gemini-1.5-pro-001"

# Get the API key from environment variables
api_key = os.getenv('GEMINI_API_KEY')

# Initialize the generative AI with the API key
genai.configure(api_key=api_key)

# Define the system instruction
# system_instruction = "hi " * 200 * 2000 # ~400,000 tokens
system_instruction = """hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi soy sauce
""" * 1580 # ~33000

message = "what is the system instruction exactly? summarize concisely. It says hi hi hi... how many times? Estimate as best as you can and give me a single number, nothing else."

# Measure time to cache the model
start_cache_time = time.time()

# Create the cached content with the system instruction
cached_content = caching.CachedContent.create(
    model=model,
    system_instruction=system_instruction,
    ttl=datetime.timedelta(minutes=5),
)

end_cache_time = time.time()

# Use the cached content to create a model
model_cached = genai.GenerativeModel.from_cached_content(cached_content=cached_content)

# Measure response with caching
start_time_caching = time.time()

# Start a chat session with caching
chat_session_cached = model_cached.start_chat(
    history=[]
)

response_cached = chat_session_cached.send_message(message)
end_time_caching = time.time()

# Measure response without caching
start_time_no_caching = time.time()

# Create the model without caching
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model_no_caching = genai.GenerativeModel(
    model_name=model,
    generation_config=generation_config,
    system_instruction=system_instruction,
)

# Start a chat session without caching
chat_session_no_caching = model_no_caching.start_chat(
    history=[]
)

response_no_caching = chat_session_no_caching.send_message(message)
end_time_no_caching = time.time()

# Print results
print("Time to cache the model:", end_cache_time - start_cache_time)
print("Caching response time:", end_time_caching - start_time_caching)
print("Response with caching:", response_cached.text)

print("No caching response time:", end_time_no_caching - start_time_no_caching)
print("Response without caching:", response_no_caching.text)
