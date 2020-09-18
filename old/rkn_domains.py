import sys
import requests
import threading
import argparse
from datetime import datetime, timedelta
from lxml.html import fromstring

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-t', '--thread')
    parser.add_argument ('-f', '--file', default='contrib/urls')
    return parser

def funcname(s,n):
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
                r = requests.get('http://'+url, timeout=2.5)
                tree = fromstring(r.content)
                text = tree.findtext('.//title')
                tag = 'TTK :: Доступ к ресурсу ограничен'
                if text != tag:
                    not_blockd.append(x)
                
            except requests.exceptions.ConnectionError:
                count_all = int(count_all) + 1
                conn_error = int(conn_error) + 1

    print('********************************************************************')
    print(threading.currentThread().getName() + ': thread end...')
    print('Проверено записей: '+str(count_all))
    #print('C ошибкой 404 : '+str(error_404_list)+' | с ошибкой подключения : '+str(conn_error)+' | с ошибкой 403 : '+str(error_403_list))
    print('Не прошли проверку : ',len(not_blockd))
    for item in not_blockd:
        out_f.write(item)


if __name__ == '__main__':
    #Аргумент '-t', '--thread', '-f', '--file',
    parser = createParser()
    items = parser.parse_args(sys.argv[1:])

    count = len(open(items.file).readlines())
    print('Процесс запусщен : ',datetime.strptime(str(datetime.now())[:-7], "%Y-%m-%d %H:%M:%S"))
    print('Записей найдено : ',count)
    drop = int(items.thread)
    ln = 0
    x = int(count/int(drop))+1
    out_f = open('nb_domain','w+')
    for i in range(int(drop)):
        my_thread = threading.Thread(target=funcname, name='Thread_'+str(i+1), args=(int(ln),int(ln+x+1)))
        my_thread.start()
        print('Thread '+str(i+1) + ' : thread start...')
        ln = int(ln+x+1)
    my_thread.join()
