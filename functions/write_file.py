import os
from google.genai import types # pyright: ignore[reportMissingImports]

def write_file(working_directory, file_path, content):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_file_path):
        try:
            os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(absolute_file_path) and os.path.isdir(absolute_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(absolute_file_path, "w") as f:
            f.write(content)
        return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return f"Error: writing to file: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file (relative to working directory)."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file."
            ),
        },
        required = ["file_path", "content"]
    ),
)