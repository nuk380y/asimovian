import os
import subprocess


def run_python_file(working_directory, file_path):
    full_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_file):
        return f'Error: File "{file_path}" not found.'
    elif not full_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    else:
        result = ""
        try:
            result = subprocess.run(
                    ["python", os.path.abspath(full_file)],
                    timeout=30,
                    capture_output=True,
                    cwd=os.path.abspath(working_directory),
                )
        except e:
            return f"Error: executing Python file: {e}"

        full_output = ""
        stdout = f"STDOUT: {result.stdout.decode('utf-8')}"
        stderr = f"STDERR: {result.stderr.decode('utf-8')}"

        if result.stdout == b"" and result.stderr == b"":
            return "No output produced."
        else:
            full_output = stdout + stderr
        
        if result.returncode != 0:
            return full_output + f"Process exited with code {result.returncode}"
        else:
            return full_output
