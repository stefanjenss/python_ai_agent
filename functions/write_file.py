import os
from google.genai import types

def write_file(
        working_directory: str, 
        file_path: str, 
        content: str
) -> str:
    try:
        # Get the absolute path of the working_directory
        working_dir_abs = os.path.abspath(working_directory)
        # Get the path of the file_path
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Check to make sure the working_directory is contained in the file_path
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        # Ensure all parent directories of the `file_path` exist
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        # Open the file_path file in write mode and overwrite the contents
        with open(file_path_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: issue writing contents to "{file_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. It is not optional",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write--or to be used to overwrite--the contents of a specified file. It is not optional"
            )
        },
        required=[
            "file_path",
            "content"
        ],
    ),
)
