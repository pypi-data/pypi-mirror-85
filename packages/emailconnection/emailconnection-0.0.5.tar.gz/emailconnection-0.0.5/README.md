FTP Adapter for Connection and Query Handling


## System Dependency

* Python 3.6.8
* pipenv


## Development Setup

1) Clone the repo 
2) cd emailconnection
3) pipenv install
4) pipenv shell

Start developing

# Package emailconnection
python version must be 3.6.8
### Build
python setup.py build

### Distribute
python setup.py sdist

### Dependency

### Use 
It wil load environment variable automatically, so all you need to do is make sure these environment variables are present. 
It will also autoload .env ( example .env.dist , rename it to .env) file before running, so you can also put these variables in your .env file. 

Needed Environment variables are 

```

# Email
GMAIL_USER=**********
GMAIL_PASSWORD=**********
#GMAIL_BYPRICE=yogesh@byprice.com,yogeshandyogi@gmail.com - this willbe hidden from user
GMAIL_CC=**********not_compulsory_or_coma_seperated
GMAIL_BCC=**********not_compulsory_or_coma_seperated
GMAIL_HOST=**********
GMAIL_PORT=**********

```

```
from emailconnection import EmailConnection 
from emailconnection.email_quiries import send_mail 
When all done , please do 

connection = EmailConnection()

# send_from will be GMAIL_USER or args passed in set conection
send_mail(connection, send_to_addressee=["kagat52553@lanelofte.com"], subject="subject", body="body")
defaults send_mail(connection, send_to_addressee, subject, body, attachment=None, extra_send=Config.GMAIL_BYPRICE, cc=Config.GMAIL_CC, bcc=Config.GMAIL_BCC)


```

## Notes 
If GMAIL_BYPRICE is present, it will added to send_list but the main sender [0] will not know. it will be added to real bcc, the user will not know 
If GMAIL_CC is present  or passed in creating connection, cc will be added after converting it to list from comma separating string
If GMAIL_BCC is present passed in creating connection, bcc will be added after converting it to list from comma separating string
