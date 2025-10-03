import os
import subprocess
from google.genai import types # pyright: ignore[reportMissingImports]

def run_python_file(working_directory, file_path, args=None):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python", absolute_file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(commands, capture_output=True, text=True, timeout=30, cwd=absolute_working_directory, )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."        

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in the working directory with optional args.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the .py file to run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments.",
            ),
        },
        required=["file_path"],
    ),
)