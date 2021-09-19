import os

from django.core.mail import send_mail
from django.conf import settings


class Mailer:
    RECIPIENTS_PATH = os.path.join(settings.RESOURCES_PATH, 'recipients.txt')
    SUBJECT_PATH = os.path.join(settings.RESOURCES_PATH, 'subject.txt')
    BODY_PATH = os.path.join(settings.RESOURCES_PATH, 'body.txt')
    LAST_INDEX_PATH = os.path.join(settings.RESOURCES_PATH, 'last_index.txt')

    def __init__(self):
        self.recipients = None
        self.subject = None
        self.body = None
        self.attachments = None

    def configure(self):
        pass

    def load(self):
        with open(self.RECIPIENTS_PATH) as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
        self.recipients = lines
        self.subject = self.open_and_read(self.SUBJECT_PATH)
        self.body = self.open_and_read(self.BODY_PATH)

    def run(self):
        count = 0
        for recipient in self.recipients:
            try:
                send_mail(self.subject,
                          self.body,
                          settings.EMAIL_HOST_USER,
                          [recipient])
                count += 1
            except Exception as e:
                print(e)
        return count / len(self.recipients)

    @staticmethod
    def open_and_read(fname):
        with open(fname) as f:
            data = f.read().strip()
        return data


def run():
    m = Mailer()
    m.load()
    m.run()
