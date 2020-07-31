import re, os, time, tqdm, multiprocessing
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from multiprocessing import Pool
from bs4 import BeautifulSoup as bs
from functools import partial
from colorama import init, deinit
from colorama import Fore, Back, Style

MAX_PERIPHERY = 150 # 문단이 너무 길 때 몇 자까지 보여주시겠습니까?

# TARGET FUNCTION
def print_result(raw_file, corpus_path, target_raw, target_comp, print_option, print_path):
    with open(''.join([corpus_path, raw_file]), 'r', encoding = 'utf-16') as f:
        raw = f.read()
        if raw == None: return
        if re.search(target_comp, raw):
            soup = bs(raw, 'html.parser')

            try: idno = soup.find('idno').text
            except: idno = ''
            try: body_list = soup.findAll('body')
            except: body_list = []

            for body in body_list:
                if body.find('date'): date = body.find('date').text
                else: date = ''
                if body.find('head'): head = body.find('head').text
                else: head = ''
                paragraphs = body.select('p')

                if re.search(target_comp, head): # <head></head> 태그에서
                    if print_option == 1:
                        search_result = set(re.findall(target_comp, head))
                        print('Process ID: ' + str(os.getpid()))
                        for res in search_result:
                            print(re.sub(res, Fore.GREEN + res + Style.RESET_ALL, head))
                    else:
                        it = re.finditer(target_comp, head)
                        span_list = [i.span() for i in it]
                        with open(print_path, 'a', encoding = 'utf-16') as html:
                            html.write('<p>{}<br />'.format(raw_file))
                            for idx in range(len(span_list)):
                                html.write('<span style="color: #ff0000;">')
                                html.write(head[span_list[idx][0] : span_list[idx][1]])
                                html.write('</span>')
                                if idx != len(span_list) - 1:
                                    html.write(head[span_list[idx][1] : span_list[idx+1][0]])
                                else:
                                    html.write('</p>')
                        
                for paragraph in paragraphs: # <p></p> 태그에서
                    if re.search(target_comp, paragraph.text): # 출력할 건덕지가 있다면
                        if print_option == 1:   # 옵션 == 1
                            search_result = set(re.findall(target_comp, paragraph.text))
                            print('Process ID: ' + str(os.getpid()))
                            for res in search_result:
                                print(re.sub(res, Fore.GREEN + res + Style.RESET_ALL, paragraph.text))
                        else:                   # 옵션 == 2
                            it = re.finditer(target_comp, paragraph.text)
                            span_list = [i.span() for i in it] # [(0, 5), (16, 21), (32, 37), (42, 47)]
                            with open(print_path, 'a', encoding = 'utf-16') as html:
                                html.write('<p><span style="color: #BDBDBD;"><a style="color: #BDBDBD;" href="{file_path}" target="_blank" rel="noopener">{file_name}</a></span><br />'.format(
                                    file_path = ''.join([corpus_path, raw_file]), file_name = raw_file))

                                # span[0][0] 이전
                                if span_list[0][0] != 0:
                                    if span_list[0][0] > MAX_PERIPHERY:
                                        html.write(paragraph.text[span_list[0][0] - MAX_PERIPHERY : span_list[0][0]])
                                    else:
                                        html.write(paragraph.text[0 : span_list[0][0]])

                                # 사이의 것들
                                for idx in range(len(span_list)):
                                    # in search
                                    html.write('<span style="color: #86E57F;">')
                                    html.write(paragraph.text[span_list[idx][0] : span_list[idx][1]])
                                    html.write('</span>')

                                    # out of search
                                    if idx != len(span_list) - 1:
                                        if span_list[idx+1][0] - span_list[idx][1] > MAX_PERIPHERY * 2:
                                            html.write(paragraph.text[span_list[idx][1] : span_list[idx][1] + MAX_PERIPHERY])
                                            html.write(' [SYSTEM: 생략된 부분입니다] ')
                                            html.write(paragraph.text[span_list[idx+1][0] - MAX_PERIPHERY : span_list[idx+1][0]])
                                        else:
                                            html.write(paragraph.text[span_list[idx][1] : span_list[idx+1][0]])
                                    else: # 마지막일 때
                                        if len(paragraph.text) - span_list[idx][1] > MAX_PERIPHERY:
                                            html.write(paragraph.text[span_list[idx][1] : span_list[idx][1] + MAX_PERIPHERY])
                                        else:
                                            html.write(paragraph.text[span_list[idx][1] : len(paragraph.text)])
                                        html.write('</p>')

if __name__ == '__main__':
    # colorama
    init()

    print()
    print('Searcher for corpus database in NIKL')
    print('Version: 2.21, Last Updated: 2020. 7. 29')
    print('업데이트 다운로드: https://www.github.com/berry2971')
    print()
    print('실행 환경 검사')
    print('Number of CPU Cores: %d' % os.cpu_count())
    print()
    print(Fore.YELLOW + '출력 옵션을 선택하세요.', end = '')
    print(Style.RESET_ALL)
    print()
    print('   1. 화면에 출력')
    print('   2. 파일로 출력(권장)')
    print()

    # set print option
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
    print_path_org = ''

    # dialog
    root = tk.Tk()
    root.withdraw()

    print()
    print(Fore.YELLOW + '코퍼스가 있는 폴더를 선택하세요.' + Style.RESET_ALL)
    print()
    corpus_path = filedialog.askdirectory()
    corpus_path = corpus_path+'\\'
    raw_files = os.listdir(corpus_path)
    raw_files = [f for f in raw_files if f.endswith('txt')]

    if print_option == 2:
        print(Fore.YELLOW + '결과물을 저장할 폴더를 선택하세요.'+ Style.RESET_ALL)
        print_path_root = filedialog.askdirectory()
        print_path_org = ''.join([print_path_root, '\\', datetime.now().strftime('%Y%m%d-%H%M%S')])
        print('결과물 저장 디렉터리: ', end = '')
        print(re.sub(r'/', r'\\', print_path_root))
        print()
        
    root.destroy()
    while(True):
        print_path = print_path_org
        print(Fore.CYAN + '검색할 정규표현식 입력: ' + Style.RESET_ALL, end = '')
        target_raw = input()
        target_comp = re.compile(target_raw)
        file_name = target_raw
        file_name = re.sub(r'[<>:"/\\|?*]', '', target_raw)
        print_path = ''.join([print_path, '-', file_name, '.html'])
        if print_option == 2:
            with open(print_path, 'a', encoding = 'utf-16') as html:
                html.write('''<!DOCTYPE html>
                <html lang="ko">
                <head>
                <meta charset="utf-16">
                <title>출력 결과: %s</title>
                <style>
                    div.pa {
                        padding: 0px 1000px 15px 15px
                    }
                    
                    body {background-color: #000000;}
                    p {color: #FFFFFF;}
                </style>
                </head>
                <body>
                <div class="pa">
                '''%target_raw
                )

        start_time = time.time()
        pool = Pool(processes = multiprocessing.cpu_count())
        func = partial(print_result, corpus_path=corpus_path, target_raw=target_raw, target_comp=target_comp, print_option=print_option, print_path=print_path)
        for _ in tqdm.tqdm(pool.imap_unordered(func, raw_files), total = len(raw_files)):
            pass
        end_time = time.time()
        print('%s초 소요되었습니다.\n' % round(end_time - start_time, 5))
        pool.close()
        pool.join()
    
        if print_option == 2:
            with open(print_path, 'a', encoding = 'utf-16') as html:
                html.write('''</div>
                </body>
                </html>''')