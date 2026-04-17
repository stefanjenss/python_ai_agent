import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # Get the absolute path of the working_directory
        working_dir_abs = os.path.abspath(working_directory)
        # Get the path of the file_path
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Check to make sure the working_directory is contained in the file_path
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # Read the file_path contents up to 10,000 characters
        with open(file_path_abs, "r") as f:
            file_path_contents = f.read(MAX_CHARS)
            # Check if the file was larger than the limit
            if f.read(1):
                file_path_contents += (
                        f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_path_contents
    except Exception as e:
        return f"Error reading file path '{file_path}: '{e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the contents (at most {MAX_CHARS} characters) of a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to working directory. It is not optional",
            ),
        },
        required=["file_path"],
    ),
)
