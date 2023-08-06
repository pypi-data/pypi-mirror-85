import smtplib
import os
from emailconnection import logger, Config


class EmailConnection:
    def __init__(self):
        logger.debug('Initiating Email Connection Class')
        self._connection_parameter = None
        self._connection = None
        self._credentials = None

    def set_connection_parameter(self, **kwargs):
        self._connection_parameter = {
            "USER": Config.GMAIL_USER if not kwargs.get('GMAIL_USER') else kwargs.get('GMAIL_USER'),
            "PASSWORD": Config.GMAIL_PASSWORD if not kwargs.get('GMAIL_PASSWORD') else kwargs.get('GMAIL_PASSWORD'),
            "CC": Config.GMAIL_CC if not kwargs.get('GMAIL_CC') else kwargs.get('GMAIL_CC'),
            "BCC": Config.GMAIL_BCC if not kwargs.get('GMAIL_BCC') else kwargs.get('GMAIL_BCC'),
            "HOST": Config.GMAIL_HOST if not kwargs.get('GMAIL_HOST') else kwargs.get('GMAIL_HOST'),
            "PORT": Config.GMAIL_PORT if not kwargs.get('GMAIL_PORT') else kwargs.get('GMAIL_PORT')
        }

    def connection(self, reconnect=False):
        if self._connection_parameter is None:
            self.set_connection_parameter()
        if self._connection is None:
            self.set_connection()
        if self._connection is None or reconnect:
            self.set_connection()
        return self._connection

    def set_connection(self):
        try:
            connection = smtplib.SMTP(self._connection_parameter['HOST'], self._connection_parameter['PORT'])
            connection.ehlo()
            connection.starttls()
            connection.login(self._connection_parameter['USER'], self._connection_parameter['PASSWORD'])
            self._connection = connection
        except Exception as e:
            logger.error(f'Connection Failed, '
                         f'user={self._connection_parameter["USER"]}, host={self._connection_parameter["HOST"]}',
                         exc_info=True)

        logger.info('Connected to Email Service')

    def execute(self, send_from_addressee, send_to_addressee, msg):
        response = False
        try:
            response = self._connection.sendmail(send_from_addressee, send_to_addressee, msg.as_string())
            logger.info(f'Tried to send email to {send_to_addressee}')
            return response
        except Exception as e:
            self.connection()
            logger.info('Forcefully Connected to Email Service')
            try:
                response = self._connection.sendmail(send_from_addressee, send_to_addressee, msg.as_string())
                logger.info(f'Tried to send email to {send_to_addressee}')
                return response
            except Exception as e:
                logger.critical('Unable to send email', exc_info=True)

        return response

    def close_connection(self):
        if self._connection is not None:
            self._connection = None
