import os

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.join(abs_working_directory, file_path)
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.stat(abs_file_path).st_size > MAX_CHARS:
                file_content_string = file_content_string + f'...File "{file_path}" truncated at 10000 characters'
            return file_content_string
    except Exception as e:
        return f"Error occured: {e}"