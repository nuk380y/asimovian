import os


def write_file(working_directory, file_path, content):
    full_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_file):
        os.makedirs(os.path.dirname(full_file), exist_ok=True)

    with open(full_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
