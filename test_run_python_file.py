from typing import List, Optional
from functions.run_python_file import run_python_file

def run_test(
        working_directory: str = "calculator",
        file_path: str = "",
        args: Optional[List[str]] = None
):
    test_out = run_python_file(working_directory, file_path, args)
    print(test_out)

run_test("calculator", "main.py")
run_test("calculator", "main.py")
run_test("calculator", "main.py", ["3 + 5"])
run_test("calculator", "tests.py")
run_test("calculator", "../main.py")
run_test("calculator", "nonexistent.py")
run_test("calculator", "lorem.txt")






