from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

## For `get_files_info`
# print(f'{get_files_info("calculator", ".")}')
# print(f'{get_files_info("calculator", "pkg")}')
# print(f'{get_files_info("calculator", "/bin")}')
# print(f'{get_files_info("calculator", "../")}')

## For `get_file_content`
print(f'{get_file_content("calculator", "lorem.txt")}')
