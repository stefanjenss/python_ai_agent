from functions.get_file_content import get_file_content

def main():
# Tests
    test_1_string = get_file_content("calculator", "main.py")
    print(f"""
    Results for 'main.py' file:
    {test_1_string}
    """)

    test_2_string = get_file_content("calculator", "pkg/calculator.py")
    print(f"""
    Results for 'pkg/calculator.py' file:
    {test_2_string}
    """)

    test_3_string = get_file_content("calculator", "/bin/cat")
    print(f"""
    Results for '/bin/cat' file:
    {test_3_string}
    """)

    test_4_string = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"""
    Results for 'pkg/does_not_exist.py' file:
    {test_4_string}
    """)

if __name__ == "__main__":
    main()
