# Website blocking quality control
Для выгрузки файлов взял за основу ```extfilter_maker.pl```
Правим под себя строчку в ```extfilter_maker.conf```

[DB]
### адрес сервера mysql
host = 'ip_address_db'
### имя пользователя
user = 'zapret'
### пароль
password = '123321'
### имя БД
name = 'rkn'

```sh
pip install -r req.txt
```
Запускается так : ``` python3 rkn_urls.py```
