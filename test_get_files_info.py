from functions.get_files_info import get_files_info

def main():
# Tests
    test_1_string = get_files_info("calculator", ".")
    print(f"""
    Results for current directory:
    {test_1_string}
    """)

    test_2_string = get_files_info("calculator", "pkg")
    print(f"""
    Results for 'pkg' directory:
    {test_2_string}
    """)

    test_3_string = get_files_info("calculator", "/bin")
    print(f"""
    Results for '/bin' directory:
    {test_3_string}
    """)

    test_4_string = get_files_info("calculator", "../")
    print(f"""
    Results for '../' directory:
    {test_4_string}
    """)

if __name__ == "__main__":
    main()
