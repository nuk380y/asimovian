from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

## For `get_files_info`
# print(f'{get_files_info("calculator", ".")}')
# print(f'{get_files_info("calculator", "pkg")}')
# print(f'{get_files_info("calculator", "/bin")}')
# print(f'{get_files_info("calculator", "../")}')

## For `get_file_content`
## Lorem Ipsum test
# print(f'{get_file_content("calculator", "lorem.txt")}')
## Standard tests
print(f'{get_file_content("calculator", "main.py")}')
print(f'{get_file_content("calculator", "pkg/calculator.py")}')
print(f'{get_file_content("calculator", "/bin/cat")}')
