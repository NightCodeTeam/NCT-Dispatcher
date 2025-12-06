from os import remove
from os.path import exists
from core.debug import create_log


def delete_file(path_to_file: str) -> bool:
    if exists(path_to_file):
        remove(path_to_file)
        create_log(f'File deleted: {path_to_file}')
        return True
    create_log(f'File NOT deleted > Not exists: {path_to_file}')
    return False
