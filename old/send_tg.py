import imaplib
import email
from email.header import decode_header
import requests

# Telegram
Token = 'XXX:YYY'
chat_id = "-XXXXXXXXXXXXXX"

# connect to yandex.ru pochta

username = "email_address"
password = "passwd_to_mail"
imap_ssl_host = 'imap.yandex.ru'
imap_ssl_port = 993
imap = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
imap.login(username, password)
status, messages = imap.select("INBOX")

messages = int(messages[0])
print(messages)
N = int(messages) # общее количество писем
for i in range(messages, messages-N, -1):
    # получить сообщение электронной почты по ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # анализировать байтовое электронное письмо в объект сообщения
            msg = email.message_from_bytes(response[1])
            # если сообщение электронной почты составное
            if msg.is_multipart():
                # перебирать части письма
                for part in msg.walk():
                    # извлечь тип содержимого электронной почты
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # получить тело письма
                        body = part.get_payload(decode=True).decode('cp1251')
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # если text/plain отправить электронные письма и пропускать вложения
                        data_tg = {
                        'chat_id': '-1001306553106',
                        'text': body
                        }
                        response = requests.post('https://api.telegram.org/bot'+Token+'/sendMessage', data=data_tg)
                        imap.store(str(i), '+FLAGS', '\\Deleted')
                        imap.expunge()
            else:
                # извлечь тип содержимого электронной почты
                content_type = msg.get_content_type()
                # получить тело письма
                body = msg.get_payload(decode=True).decode('cp1251')
                if content_type == "text/plain":
                    # отправить только текстовые части электронного письма
                    data_tg = {
                    'chat_id': '-1001306553106',
                    'text': '```'+str(body)+'```'
                    }
                    response = requests.post('https://api.telegram.org/bot'+Token+'/sendMessage', data=data_tg)
            imap.store(str(i), '+FLAGS', '\\Deleted')
            imap.expunge()    
imap.close()
imap.logout()
