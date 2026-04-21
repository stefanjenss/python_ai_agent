from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.get_file_content import get_file_content, schema_get_file_content

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ],
)


def call_function(
    function_call: types.FunctionCall,
    verbose: bool = False
) -> types.Content:
    if verbose == True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Define a mapping of function names to the actual functions
    function_map: dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name: str = function_call.name or "" # ~ In theory, the function_call can be `None`, so copy it to a variable to guarantee a string

    # If the function_name is not found in function_map, return a types.Content with an error
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                ),
            ],
        )

    # Handle the provided arguments
    args: dict = dict(function_call.args) if function_call.args else {}

    # Set the working directory in the args dictionary
    args["working_directory"] = "./calculator"

    # Call the function and store the results
    function_result: str = function_map[function_name](**args)

    # Return the contents of the function call
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}, # ~ Because from_function_response requires the response to be a dictionary, we just shove the string result into a "result" field
            ),
        ],
    )
