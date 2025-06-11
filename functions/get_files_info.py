import os


def get_files_info(working_directory, directory=None):
    directory = os.path.join(working_directory, directory)

    if not os.path.abspath(directory).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    else:
        sub_directories = os.listdir(os.path.abspath(directory))
        output = []

        for file in sub_directories:
            file = os.path.join(directory, file)
            filename = os.path.basename(file)
            filesize = os.path.getsize(os.path.abspath(file))
            is_dir = os.path.isdir(os.path.abspath(file))
            output.append(f"- {filename}: filesize={filesize} bytes, is_dir={is_dir}")

        return "\n".join(output)
