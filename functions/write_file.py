import os


def write_file(working_directory, file_path, content):
    full_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_file):
        pass
        
        ## NOTES
        # If this code runs, it's because the _file_ doesn't exist.  Should
        # probably verify if the directory path exists as well.  If this takes
        # too long, consult with Boots.
    else:
        with open(full_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
