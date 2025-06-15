import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You
can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to teh working directory.  You do not
need to specify the working directory in your function calls as it is
automatically injected for security reasons.
"""

# Describe the available functions.
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to list files from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified Python script, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to Python script to run, relative to the working directory. STDOUT and STDERR will both be output to the terminal. If exit-code is non-zero, it also will be output to the terminal.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Read the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory. If file already exists, contents will be overwritten.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
            ),
        },
    ),
)

# Define the described functions as tools available to the LLM.
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    allowed_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    actual_function = ""
    result = ""

    if function_call_part.name not in allowed_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    else:
        actual_function = allowed_functions[function_call_part.name]
        function_call_part.args.update({"working_directory": "./calculator"})
        result = actual_function(**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
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
if verbose:
    print(f"User prompt: {user_prompt}\n")

# Define Generative AI (genai) client with locally stored API key
client = genai.Client(api_key=api_key)

for count in range(0, 19):
    func_called = False
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

        for part in candidate.content.parts:
            if part.function_call:
                function_result = call_function(part.function_call, verbose)
                messages.append(function_result)
                func_called = True

    if not func_called:
        final_text = response.text
        if final_text:
            print("Final response:")
            print(final_text)
            break

## I think the loop structure above nullifies this commented block...
# funcs = response.function_calls
#
# # Print the text of the response...
# if response.text != None:
#     print(f"{response.text}")
# else:
#     print("")
#
# if funcs:
#     for call in funcs:
#         generates_content = call_function(call, verbose)
#
#         try:
#             if verbose:
#                 print(f"-> {generates_content.parts[0].function_response.response['result']}")
#         except:
#             raise Exception("no function response presented")

if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
