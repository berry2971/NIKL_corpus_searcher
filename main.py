import re, os, time, tqdm, multiprocessing
import tkinter as tk
from multiprocessing import Pool
from bs4 import BeautifulSoup as bs
from functools import partial
from colorama import init, deinit
from colorama import Fore, Back, Style

from pkg.html import *
from pkg.greeting import *
from pkg.getOption import *
from pkg.searching import *
from pkg.printResult import *

MAX_PERIPHERY = 150 # 문단이 너무 길 때 몇 자까지 보여주시겠습니까?

if __name__ == '__main__':
    init() # colorama

    greeting()

    # get print_option
    print_option = get_print_option()

    # ready for dialog
    root = tk.Tk()
    root.withdraw()

    # get corpus_path_root, raw_files
    corpus_path_root = get_corpus_path_root()
    raw_files = [f for f in os.listdir(corpus_path_root) if f.endswith('txt')]

    # get print_path_root
    print_path_root = ''
    if print_option == 2:
        print_path_root = get_print_path_root()
        print('결과물 저장 디렉터리: ' + re.sub(r'/', r'\\', print_path_root))
        print()

    # destroy for dialog
    root.destroy()

    while(True):
        # get search target
        target_raw = get_target_raw()
        target_comp = re.compile(target_raw)
        result_file = create_result_file(print_path_root, target_raw) # ~.html

        # HTML 모드일 때 head 부분 출력
        if print_option == 2:
            with open(result_file, 'a', encoding = 'utf-16') as html:
                html.write(html_head(target_raw))

        # start searching
        start_time = time.time()
        pool = Pool(processes = multiprocessing.cpu_count())
        func = partial(
            print_result,
            corpus_path_root=corpus_path_root,
            target_comp=target_comp,
            print_option=print_option,
            result_file=result_file,
            MAX_PERIPHERY=MAX_PERIPHERY
            )
        for _ in tqdm.tqdm(pool.imap_unordered(func, raw_files), total = len(raw_files)):
            pass

        # end searching
        end_time = time.time()
        print("%s초 소요되었습니다.\n" % round(end_time - start_time, 5))
        pool.close()
        pool.join()
    
        # HTML 모드일 때 tail 부분 출력
        if print_option == 2:
            with open(result_file, 'a', encoding = 'utf-16') as html:
                html.write(html_tail())