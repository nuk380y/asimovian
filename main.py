import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
verbose = False

if len(sys.argv) == 1:
    print("No prompt entered")
    sys.exit(1)
elif len(sys.argv) >= 3:
    if sys.argv[-1] == "--verbose":
        verbose = True
    else:
        raise Exception(f"{sys.argv[-1]}: not recognized")

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Define Generative AI (genai) client with locally stored API key
client = genai.Client(api_key=api_key)
# Create variable to receive response from specified LLM
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

if verbose:
    print(f"User prompt: {user_prompt}\n")
# Print the text of the response...
print(f"{response.text}")
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
