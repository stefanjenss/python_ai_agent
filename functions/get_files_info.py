import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)

def get_files_info(working_directory, directory = "."):
    try:
        # Get the absolute path of the working_directory
        working_dir_abs = os.path.abspath(working_directory)
        # Get the path of the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Check to make sure the working_directory is contained in the target directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        list_of_strings = []
        # Iterate over the items in the target directory
        for item in os.listdir(target_dir):
            current_strings = ""
            current_item_path = os.path.join(target_dir, item)
            # For each item, record the name, file size, and whether it's a directory itself
            current_strings = (current_strings +
                f"- {item}: " + 
                f"file_size={os.path.getsize(current_item_path)} bytes, " +
                f"is_dir={os.path.isdir(current_item_path)}"
            )
            list_of_strings.append(current_strings)
        # Return the string represation of target_dir
        return "\n".join(list_of_strings)
    except Exception as e:
        return f"Error: {e}"

