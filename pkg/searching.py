from colorama import Fore, Back, Style
import re
from datetime import datetime

def get_target_raw():
    print(Fore.CYAN + '검색할 정규표현식 입력: ' + Style.RESET_ALL, end = '')
    target_raw = input()

    return target_raw

def create_result_file(print_path_root, target_raw):
    file_name = re.sub(r'[<>:"/\\|?*]', '', target_raw)
    temp = ''.join([print_path_root, '\\', datetime.now().strftime('%Y%m%d-%H%M%S')])
    result_file = ''.join([temp, '-', file_name, '.html'])

    return result_file