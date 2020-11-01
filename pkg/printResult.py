import re, os
from bs4 import BeautifulSoup as bs
from colorama import init, deinit
from colorama import Fore, Back, Style

def display_html_paragraph(target_comp, paragraph, result_file, corpus_path_root, raw_file, MAX_PERIPHERY):
    it = re.finditer(target_comp, paragraph)
    span_list = [i.span() for i in it] # [(0, 5), (16, 21), (32, 37), (42, 47)]
    with open(result_file, 'a', encoding = 'utf-16') as html:
        html.write(
            '''<p><span style="color: #BDBDBD;">
            <a style="color: #BDBDBD;" href="{file_path}" target="_blank" rel="noopener">{file_name}</a>
            </span><br />'''.format(
                file_path = ''.join([corpus_path_root, raw_file]), file_name = raw_file
                )
            )

        # span[0][0] 이전
        if span_list[0][0] != 0:
            if span_list[0][0] > MAX_PERIPHERY:
                html.write(paragraph[span_list[0][0] - MAX_PERIPHERY : span_list[0][0]])
            else:
                html.write(paragraph[0 : span_list[0][0]])

        # 사이의 것들
            for idx in range(len(span_list)):
                # in search
                html.write('<span style="color: #86E57F;">')
                html.write(paragraph[span_list[idx][0] : span_list[idx][1]])
                html.write('</span>')

                # out of search
                if idx != len(span_list) - 1:
                    if span_list[idx+1][0] - span_list[idx][1] > MAX_PERIPHERY * 2:
                        html.write(paragraph[span_list[idx][1] : span_list[idx][1] + MAX_PERIPHERY])
                        html.write(' [SYSTEM: 생략된 부분입니다] ')
                        html.write(paragraph[span_list[idx+1][0] - MAX_PERIPHERY : span_list[idx+1][0]])
                    else:
                        html.write(paragraph[span_list[idx][1] : span_list[idx+1][0]])
                else: # 마지막일 때
                    if len(paragraph) - span_list[idx][1] > MAX_PERIPHERY:
                        html.write(paragraph[span_list[idx][1] : span_list[idx][1] + MAX_PERIPHERY])
                    else:
                        html.write(paragraph[span_list[idx][1] : len(paragraph)])
                    html.write('</p>')

def display_html_head(target_comp, head, result_file, raw_file):
    it = re.finditer(target_comp, head)
    span_list = [i.span() for i in it]
    with open(result_file, 'a', encoding = 'utf-16') as html:
        html.write('<p>{}<br />'.format(raw_file))
        for idx in range(len(span_list)):
            html.write('<span style="color: #ff0000;">')
            html.write(head[span_list[idx][0] : span_list[idx][1]])
            html.write('</span>')
            if idx != len(span_list) - 1:
                html.write(head[span_list[idx][1] : span_list[idx+1][0]])
            else:
                html.write('</p>')

def display_console(target_comp, element):
    search_result = set(re.findall(target_comp, element))
    print('Process ID: ' + str(os.getpid()))
    for res in search_result:
        print(re.sub(res, colorText("green", res), element))

def colorText(color, text): # 콘솔에서 색을 바꾼 텍스트를 반환
    if color == "green":
        return Fore.GREEN + text + Style.RESET_ALL

# TARGET FUNCTION
def print_result(raw_file, corpus_path_root, target_comp, print_option, result_file, MAX_PERIPHERY):
    with open(''.join([corpus_path_root, raw_file]), 'r', encoding = 'utf-16') as f:
        raw = f.read() # f is single raw corpus file
        if raw == None: return
        if re.search(target_comp, raw) == None: return

        soup = bs(raw, 'html.parser')

        try: body_list = soup.findAll('body')
        except: return

        for body in body_list:
            # select head
            if body.find('head'):
                head = body.find('head').text
            else: head = ''

            # select paragraphs
            paragraphs = body.select('p')

            # SEARCH IN HEAD
            if re.search(target_comp, head): # <head></head> 태그에서
                if print_option == 1:
                    display_console(target_comp, head)
                else:
                    display_html_head(target_comp, head, result_file, raw_file)

            # SEARCH IN PARAGRAPH  
            for p in paragraphs: # <p></p> 태그에서
                paragraph = p.text
                if re.search(target_comp, paragraph): # 출력할 건덕지가 있다면
                    if print_option == 1:   # 옵션 == 1
                        display_console(target_comp, paragraph)
                    else:                   # 옵션 == 2
                        display_html_paragraph(target_comp, paragraph, result_file, corpus_path_root, raw_file, MAX_PERIPHERY)