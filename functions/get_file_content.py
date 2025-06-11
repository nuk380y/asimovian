import os


def get_file_content(working_directory, file_path):
    full_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
    elif not os.path.isfile(full_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        MAX_CHARACTERS = 10000
        file_contents = ""

        with open(full_file, "r") as f:
            file_contents = f.read(MAX_CHARACTERS)
            full_content = f.read()

            if len(full_content) > MAX_CHARACTERS:
                file_contents += (
                    f'\n\n[...File "{file_path}" truncated at 10000 characters]'
                )

        return file_contents
