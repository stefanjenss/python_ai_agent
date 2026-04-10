from functions.write_file import write_file

def main():
# Tests
    test_1_string = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"""
    Results for 'lorem.txt' file:
    {test_1_string}
    """)

    test_2_string = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"""
    Results for 'pkg/morelorem.txt' file:
    {test_2_string}
    """)

    test_3_string = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"""
    Results for '/tmp/temp.txt' file:
    {test_3_string}
    """)

if __name__ == "__main__":
    main()
