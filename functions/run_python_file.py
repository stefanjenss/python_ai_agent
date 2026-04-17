import subprocess
import os
from google.genai import types

def run_python_file(
        working_directory: str,
        file_path: str, 
        args: list[str] | None = None
) -> str:
    try:
        # Make the file path absolute
        def make_absolute(
                file_path: str,
                working_directory: str
        ) -> str:
            joined_file_path = os.path.join(working_directory, file_path)
            file_path_abs = os.path.abspath(joined_file_path)
            working_dir_abs = os.path.abspath(working_directory)

            if os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs:
                return file_path_abs

            else:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                
        absolute_file_path = make_absolute(file_path, working_directory)
        if absolute_file_path.startswith("Error"):
            return absolute_file_path
        
        # Raise error if file_path does not point to a regular file
        if not os.path.isfile(absolute_file_path):
            return (f'Error: "{file_path}" does not exist or is not a regular file')
        
        # Raise error if the file is not a .py file
        if not absolute_file_path.endswith(".py"):
            return (f'Error: "{file_path}" is not a Python file')

        # Built the command to run
        command = ["python", absolute_file_path]

        # Add any provided args to the command list
        if args is not None:
            command.extend(args)

        sub_p_command = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build the output string based on the CompletedProcess
        output_string: str = ""

        if sub_p_command.returncode != 0:
            output_string = output_string + f"Process exited with code {sub_p_command.returncode}"

        if (not sub_p_command.stdout) and (not sub_p_command.stderr):
            output_string = output_string + "No output produced"
        if sub_p_command.stdout:
            output_string = output_string + f"STDOUT: {sub_p_command.stdout}\n"
        if sub_p_command.stderr:
            output_string = output_string + f"STDERR: {sub_p_command.stderr}"

        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a specified Python file within the working directory with the Python3 interpreter and return its output. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory. It is not optional",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An optional list of arguments to be passed to the Python script"
            ),
        },
        required=["file_path"],
    ),
)

