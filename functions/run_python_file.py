import os


def run_python_file(working_directory, file_path):
    full_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_file):
        return f'Error: File "{file_path}" not found.'
    elif ".py" not in full_file:
        return f'Error: "{file_path}" is not a Python file.'
    else:
        with open(full_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
