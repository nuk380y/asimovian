import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You
can perform the following operations:

- List files and directories

All paths you provide should be relative to teh working directory.  You do not
need to specify the working directory in your function calls as it is
automatically injected for security reasons.
"""

# Describe the available function.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# Define the described functions as tools available to the LLM.
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

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
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    ),
)

funcs = response.function_calls

if verbose:
    print(f"User prompt: {user_prompt}\n")

# Print the text of the response...
if response.text != None:
    print(f"{response.text}")
else:
    print("")

if funcs:
    for call in funcs:
        print(f"Calling function: {call.name}({call.args})")

if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
