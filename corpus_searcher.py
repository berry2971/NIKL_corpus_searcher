import re, os, time
import multiprocessing
from multiprocessing import Pool
import tqdm
from bs4 import BeautifulSoup as bs

# global vars
target_raw = '[해여어]도 되'
target = re.compile(target_raw)
directory = r'F:\corpus_raw_org\\'
raw_files = os.listdir(directory)

# TARGET FUNCTION
def print_result(raw_file):
    with open(''.join([directory, raw_file]), 'r', encoding = 'utf-16') as f:
        raw = f.read()
        if raw == None: return
        if re.search(target, raw):
            soup = bs(raw, 'html.parser')

            idno = soup.find('idno').text
            body_list = soup.findAll('body')

            for body in body_list:
                if body.find('date'): date = body.find('date').text
                else: date = ''
                if body.find('head'): head = body.find('head').text
                else: head = ''
                paragraphs = body.select('p')

                if re.search(target, head):
                    print('Process ID: ' + str(os.getpid()))
                    print(head)
                for paragraph in paragraphs:
                    if re.search(target, paragraph.text):
                        print('Process ID: ' + str(os.getpid()))
                        print(paragraph.text)

if __name__ == '__main__':
    print('Number of CPU Cores: %d' % os.cpu_count())
    start_time = time.time()
    pool = Pool(processes = multiprocessing.cpu_count())
    for _ in tqdm.tqdm(pool.imap_unordered(print_result, raw_files), total = len(raw_files)):
        pass
    # pool.map(print_result, raw_files)
    end_time = time.time()
    print('%s초 소요되었습니다.\n' % (end_time - start_time))
    pool.close()
    pool.join()



'''
# open file
for corpus_file in tqdm(corpus_files):
    with open(dir+corpus_file, 'r', encoding = 'utf-16') as f:
        raw = f.read()
        soup = bs(raw, 'html.parser')
        
        idno = soup.find('idno').text
        body_list = soup.findAll('body')

        for body in body_list:
            if body.find('date'): date = body.find('date').text
            if body.find('head'): head = body.find('head').text
            paragraphs = body.select('p')

            if re.search(TARGET, head): print(head)
            for paragraph in paragraphs:
                if re.search(TARGET, paragraph.text): print(paragraph.text)





f2 = open(r'D:\Private Files\Desktop\res.txt', 'w', encoding='utf-16')

for corpus_file in tqdm(corpus_files):
    with open(dir+corpus_file, 'r', encoding = 'utf-16') as f:
        raw = f.read()
        if re.search(TARGET, raw):
            f2.write(raw)
            continue
f2.close()





with open(dir+r'\2BA90A03.txt', 'r', encoding='utf16') as f:
    whole = f.read()
    soup = bs(whole, 'html.parser')
    a = soup.findAll('body')
    print(a[1].text)
'''