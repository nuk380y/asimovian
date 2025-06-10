import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Define Generative AI (genai) client with locally stored API key
client = genai.Client(api_key=api_key)
# Create variable to receive response from specified LLM
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
)

# Print the text of the response...
print(f"{response.text}")
# Followed by the number of tokens consumed by the prompt and response.
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
