from smtplib import SMTP
from email.message import EmailMessage
from quiltz.domain.results import Success, Failure
from quiltz.domain.anonymizer import anonymize
from textwrap import dedent
import ssl
import logging

class NoMessageEngine:
    def commit(self, messenger):
        pass

class SMTPBasedMessageEngine:
    @staticmethod
    def from_config(config):
        if config.FOR_TEST:
            return SMTPBasedMessageEngineForTest(config.SMTP_HOST, config.SMTP_PORT, None, None)
        else:
            return SMTPBasedMessageEngine(config.SMTP_HOST, config.SMTP_PORT, config.SMTP_USER, config.SMTP_PASSWORD)
        
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password 
        self.logger = logging.getLogger(self.__class__.__name__)

    def login(self, smtp):
        smtp.login(self.user, self.password)

    def create_ssl_context(self):
        return ssl.create_default_context()

    def commit(self, messenger):
        try:
            with SMTP(self.host, self.port) as smtp:
                smtp.starttls(context=self.create_ssl_context())
                self.login(smtp)
                for message in messenger.messages:
                    smtp.send_message(msg=as_smtp_message(message))
                self.logger.info("Flushed messages to {}".format(", ".join([ anonymize(m.to.email) for m in messenger.messages ])))
        except ConnectionError as e:
            return Failure(message=str(e))
        return Success()

class SMTPBasedMessageEngineForTest(SMTPBasedMessageEngine):

    def login(self, smtp):
        pass

    def create_ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context
        
def as_smtp_message(message):
    email_message = EmailMessage()
    email_message['To'] = message.recipient
    email_message['From'] = message.sender
    email_message['Subject'] = message.subject
    email_message.set_content(message.body)
    return email_message
