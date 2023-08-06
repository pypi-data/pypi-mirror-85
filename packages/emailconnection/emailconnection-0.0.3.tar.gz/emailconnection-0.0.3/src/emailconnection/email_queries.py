from emailconnection import Config
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(connection, send_to_addressee, subject, body, attachment=None,
              extra_send=Config.GMAIL_BYPRICE, cc=Config.GMAIL_CC, bcc=Config.GMAIL_BCC):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.environ.get('GMAIL_USER')
    msg['To'] = ';'.join(send_to_addressee)

    if extra_send:
        send_to_addressee+=extra_send
    if cc:
        msg['CC'] = ';'.join(cc)
        send_to_addressee += cc
    if bcc:
        msg['BCC'] = ';'.join(bcc)
        send_to_addressee += bcc

    generated_body = body
    html_body = MIMEText(generated_body, 'html')
    msg.attach(html_body)
    if attachment:
        part = MIMEApplication(
            attachment.get('content'),
            Name=attachment.get('name')
        )
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment.get('name'))
        msg.attach(part)
    return connection.execute(Config.GMAIL_USER, send_to_addressee, msg)
