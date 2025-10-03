import os
from config import MAX_CHARS
from google.genai import types # pyright: ignore[reportMissingImports]

def get_file_content(working_directory, file_path):
    absolute_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(target_file_path) > MAX_CHARS:
                content += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read a file's contents in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read.",
            ),
        },
        required = ["file_path"],
    ),
)