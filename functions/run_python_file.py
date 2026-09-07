

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file in the specified working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The base working directory"
                },
                "file_path": {
                    "type": "string",
                    "description": "The relative path to the file from the working directory"
                }
            },
            "required": ["working_directory", "file_path"]
        }
    }
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """
    Run a Python file in the specified working directory.

    Args:
        working_directory (str): The base working directory.
        file_path (str): The relative path to the Python file from the working directory.
        args (list[str] | None): Optional list of arguments to pass to the Python script.

    Returns:
        str: The output of the Python script or an error message if the script cannot be run.
    """
    import subprocess
    import os

    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and not stderr:
            return "No output produced"

        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}" if stderr else f"STDOUT:\n{stdout}"

    except Exception as error:
        return f"Error: executing Python file: {error}"