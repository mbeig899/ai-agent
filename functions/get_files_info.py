import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["directory"],
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Get information about files in the specified directory.

    Args:
        working_directory (str): The base working directory.
        directory (str): The target directory to scan for files. Defaults to the current directory.

    Returns:
        str: A formatted string containing information about the files in the specified directory.
    """

    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        results = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            results.append((item, file_size, is_directory))

        list_of_files = "\n".join(
            f" - {item}: file_size={file_size} bytes, is_dir={is_directory}"
            for item, file_size, is_directory in results
        )

        return f'Results for "{directory}":\n{list_of_files}'
    except Exception as error:
        return f"Error: {error}"