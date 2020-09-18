import requests
import threading
from lxml.html import fromstring

filename = 'nb_test'
count = len(open(filename).readlines())
drop = 20
print('строк в файле : ',count)
out_f = open('control','w+')
def funcname(s,n):
    for i, line in enumerate(open(filename)):
        if i >= int(s) and i <= int(n):
            try:
                url = line.strip()
                r = requests.get('http://'+url, timeout=2.5)
                tree = fromstring(r.content)
                text = tree.findtext('.//title')
                tag = 'TTK :: Доступ к ресурсу ограничен'
                if text == tag:
                    print(i,'Сайт заблокирован!')
                else:
                    print(i,'Увы , не заблокирован')
                    out_f.write(url)
            except:
                print('не могу проверить')
                out_f.write(url)

if __name__ == '__main__':
    ln = 0
    x = int(count/int(drop))
    for i in range(int(drop)):
        my_thread = threading.Thread(target=funcname, name='Thread_'+str(i), args=(int(ln),int(ln+x+1)))
        my_thread.start()
        ln = int(ln+x+1)
    my_thread.join()

