import sys
import requests
import threading
import argparse
from datetime import datetime, timedelta
from lxml.html import fromstring
from lxml.etree import ParseError
from lxml.etree import ParserError

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-t', '--thread', help="Количество потоков")
    parser.add_argument ('-f', '--file', default='contrib/urls', help="файл с которого будем забирать строки")
    parser.add_argument ('-m', '--marker', help="По какому маркеру проверять")
    parser.add_argument ('-o', '--output', help="Путь выходного файла с результатом")
    return parser

def rkn_control_dom(s,n):
    not_blockd = []
    error_404_list = 0
    error_403_list = 0
    count_blocked = 0
    count_all = 0
    conn_error = 0
    for i, x in enumerate(open(items.file)):
        if i >= int(s) and i <= int(n):
            try:
                count_all = int(count_all) + 1
                if '*.' in x:
                    url = x.strip()[2:]
                else:
                    url = x.strip()

                response_head = requests.head('http://'+url, timeout=3)

                if response_head.status_code == 301:
                    count_all = int(count_all) + 1
                    count_blocked = int(count_blocked) + 1
                elif response_head.status_code == 404:
                    count_all = int(count_all) + 1
                    error_404_list = int(error_404_list) + 1
                elif response_head.status_code == 403:
                    count_all = int(count_all) + 1
                    error_403_list = int(error_403_list) + 1
                elif response_head.status_code == 200:
                    count_all = int(count_all) + 1
                    response_get = requests.get('http://'+url, timeout=2.5)
                    tree = fromstring(response_get.content)
                    text = tree.findtext('.//title')

                    if str(items.marker) not in str(text):
                        count_all = int(count_all) + 1
                        not_blockd.append(x)
                
            except requests.exceptions.ConnectionError:
                count_all = int(count_all) + 1
                conn_error = int(conn_error) + 1
            except requests.exceptions.Timeout:
                count_all = int(count_all) + 1
                conn_error = int(conn_error) + 1
            except requests.exceptions.RequestException:
                count_all = int(count_all) + 1
                conn_error = int(conn_error) + 1
            except (ParserError, ParseError):
                count_all = int(count_all) + 1
                not_blockd.append(x)
            except UnicodeDecodeError:
                count_all = int(count_all) + 1
                not_blockd.append(x)

    print('********************************************************************')
    print(threading.currentThread().getName() + ': thread end... | ' + str(items.output))
    print('Проверено записей: '+str(count_all))
    print('C ошибкой 404 : '+str(error_404_list)+' | с ошибкой подключения : '+str(conn_error)+' | с ошибкой 403 : '+str(error_403_list))
    print('Не прошли проверку : ',len(not_blockd))
    for item in not_blockd:
        out_f.write(item)


if __name__ == '__main__':
    #Аргумент '-t', '--thread', '-f', '--file',
    parser = createParser()
    items = parser.parse_args(sys.argv[1:])

    count = len(open(items.file).readlines())
    print('Процесс запущен : ',datetime.strptime(str(datetime.now())[:-7], "%Y-%m-%d %H:%M:%S"))
    print('Записей найдено : ',count)
    drop = int(items.thread)
    ln = 0
    x = int(count/int(drop))+1
    out_f = open(items.output,'w+')
    for i in range(int(drop)):
        my_thread = threading.Thread(target=rkn_control_dom, name='Thread_'+str(i+1), args=(int(ln),int(ln+x+1)))
        my_thread.start()
        #print('Thread '+str(i+1) + ' : thread start...')
        ln = int(ln+x+1)
    my_thread.join()
    count = len(open(items.output).readlines())