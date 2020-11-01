from colorama import init, deinit
from colorama import Fore, Back, Style
from tkinter import filedialog

def get_print_option():
    # display print option
    print(Fore.YELLOW + '출력 옵션을 선택하세요.', end = '')
    print(Style.RESET_ALL)
    print()
    print('   1. 화면에 출력')
    print('   2. 파일로 출력(권장)')
    print()

    # get print option
    print_option = -1
    while(True):
        try:
            print_option = int(input('출력 옵션 선택: '))
            if print_option not in [1, 2]:
                print('잘못 입력하셨습니다.')
            else:
                break
        except:
            print('잘못 입력하셨습니다.')

    return print_option

def get_corpus_path_root():
    print()
    print(Fore.YELLOW + '코퍼스가 있는 폴더를 선택하세요.' + Style.RESET_ALL)
    print()
    corpus_path_root = filedialog.askdirectory()+'\\'

    return corpus_path_root

def get_print_path_root():
    print(Fore.YELLOW + '결과물을 저장할 폴더를 선택하세요.'+ Style.RESET_ALL)
    print_path_root = filedialog.askdirectory()

    return print_path_root