import os
import time
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

model = "gemini-1.5-flash-001"

# Read content from combined_files.txt
with open('combined_files.txt', 'r') as file:
    content = file.read()

# Create the system instruction with the content of combined_files.txt
system_instruction = f"""You are an AI assistant with knowledge of the following project content:

{content}

Please use this information to answer questions and assist with tasks related to this project."""

# Measure time to cache the model
start_cache_time = time.time()

# Create the cached content with the system instruction
cached_content = caching.CachedContent.create(
    model=model,
    system_instruction=system_instruction,
    ttl=datetime.timedelta(minutes=5),
)

end_cache_time = time.time()

print(f"Time to cache the model: {end_cache_time - start_cache_time:.2f} seconds")

# Use the cached content to create a model
model_cached = genai.GenerativeModel.from_cached_content(cached_content=cached_content)

# Start a chat session with caching
chat_session = model_cached.start_chat(history=[])

def chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("AI: Goodbye!")
            break

        start_time = time.time()
        response = chat_session.send_message(user_input)
        end_time = time.time()

        print(f"AI: {response.text}")
        print(f"Response time: {end_time - start_time:.2f} seconds")

print("Chat session started. Type 'exit', 'quit', or 'bye' to end the conversation.")
chat()
