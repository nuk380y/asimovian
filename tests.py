from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

## For `get_files_info`
# print(f'{get_files_info("calculator", ".")}')
# print(f'{get_files_info("calculator", "pkg")}')
# print(f'{get_files_info("calculator", "/bin")}')
# print(f'{get_files_info("calculator", "../")}')

## For `get_file_content`
## Lorem Ipsum test
# print(f'{get_file_content("calculator", "lorem.txt")}')
## Standard tests
# print(f'{get_file_content("calculator", "main.py")}')
# print(f'{get_file_content("calculator", "pkg/calculator.py")}')
# print(f'{get_file_content("calculator", "/bin/cat")}')

## For 'write_file`
# print(f'{write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")}')
# print(f'{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}')
# print(f'{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}')

## For 'run_python_file'
print(f'{run_python_file("calculator", "main.py")}')
print(f'{run_python_file("calculator", "tests.py")}')
print(f'{run_python_file("calculator", "../main.py")}')
print(f'{run_python_file("calculator", "nonexistent.py")}')
