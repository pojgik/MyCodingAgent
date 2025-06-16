import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    try:
        if directory is None:
            directory = working_directory
        abs_working_directory = os.path.abspath(working_directory)
        abs_directory = os.path.join(abs_working_directory, directory)
        if not abs_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'

        contents = []
        for entry in os.listdir(abs_directory):
            entry_path = os.path.join(abs_directory, entry)
            contents.append(f"- {entry}: file_size={os.path.getsize(entry_path)} bytes, is_dir={os.path.isdir(entry_path)}")
        return "\n".join(contents)
    except Exception as e:
        return f"Error occured: {e}"
    
# get_files_info
schema_get_files_info = types.FunctionDeclaration( 
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
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
