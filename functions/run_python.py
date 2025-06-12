import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if file_path[-3:] != '.py':
            f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error occured: {e}"
    try:
        result = subprocess.run(['python3', file_path], timeout=30, capture_output=True, cwd=abs_working_directory)
        if result is None:
            return "No output produced"
        output = ""
        output += f"STDOUT: {result.stdout}, STDERR: {result.stderr}"
        if (result.returncode != 0):
            output += f", Process exited with code {result.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
        