import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory",
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

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Get the content of a file in the specified working directory.

    Args:
        working_directory (str): The base working directory.
        file_path (str): The relative path to the file from the working directory.

    Returns:
        str: The content of the file or an error message if the file cannot be read.
    """
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'

        with open(target_file, "r") as file:
            content = file.read(MAX_CHARS)

        if len(content) == MAX_CHARS:
            content += f"... [truncated at {MAX_CHARS} characters]"

        return content
        
    except Exception as error:
        return f"Error: {error}"