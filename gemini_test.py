"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=api_key)

system_instruction = """hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi 
hi hi hi hi hi hi soy sauce"""

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
#   model_name="gemini-1.5-pro",
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instruction,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("the first message says hi hi... then what? what's the last word after that?")

print(response.text)