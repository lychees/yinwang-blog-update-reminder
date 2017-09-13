"""A naive spider"""
import http.client
import urllib
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

last_body = ""
CONFIG = {
    'url': 'http://www.yinwang.org/',
    'interval': 300, # in seconds
    'keyword': 'Started', # Keyword to be alerted
    'smtp': '1', # SMTP Server like: smtp.163.com
    'smtp_ssl': True, # Whether using SSL/TLS
    'smtp_port': 465, # SMTP Port
    'username': '', # SMTP Username
    'password': '', # SMTP Password
    'sender': '', # Sender E-mail Address
    'receivers': [''], # Receivers E-mail Address List
}

def send_mail(content):
    '''Send Email with given content'''
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('Spider Alert')
    message['To'] = Header('Spider Alert')
    message['Subject'] = Header('Spider Alert Detected', 'utf-8')
    try:
        if CONFIG['smtp_ssl']:
            smtp = smtplib.SMTP_SSL(CONFIG['smtp'], port=CONFIG['smtp_port'])
        else:
            smtp = smtplib.SMTP(CONFIG['smtp'], port=CONFIG['smtp_port'])
        smtp.login(CONFIG['username'], CONFIG['password'])
        smtp.sendmail(CONFIG['sender'], CONFIG['receivers'], message.as_string())
        print('Mail Sent')
    except smtplib.SMTPException as err:
        print('Error: failed to send the mail')
        print(str(err))


def detect():
    '''Detect whether html contains keyword'''
    global last_body
    try:
        url = urllib.parse.urlparse(CONFIG['url'])
        
        if url.scheme == 'http':
            connection = http.client.HTTPConnection(url.netloc)
        else:
            connection = http.client.HTTPSConnection(url.netloc)
        connection.request('GET', url.path)
        response = connection.getresponse()
        body = str(response.read())        

        t = time.asctime(time.localtime(time.time()))

        if last_body != "" and body != last_body:
            print('Updated at ' + t)

        if body.find(CONFIG['keyword']) >= 0:
            # Found the keyword
            print('Detected at ' + t)
            # send_mail(body)
        else:
            # Not found
            print('Not Found at ' + t) 
        last_body = body
    except Exception as err:
        print(str(err))

while True:
    detect()
    time.sleep(CONFIG['interval'])
