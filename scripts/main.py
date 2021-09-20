import glob
import os

from django.core.mail import send_mail
from django.conf import settings


class Mailer:
    RECIPIENTS_PATH = os.path.join(settings.RESOURCES_PATH, 'recipients.txt')
    SUBJECT_PATH = os.path.join(settings.RESOURCES_PATH, 'subject.txt')
    BODY_PATH = os.path.join(settings.RESOURCES_PATH, 'body.txt')
    LAST_INDEX_PATH = os.path.join(settings.RESOURCES_PATH, 'last_index.txt')
    ATTACHMENTS_PATH = os.path.join(settings.RESOURCES_PATH, 'attachments')
    RECIPIENTS_PER_RUN = 500

    def __init__(self):
        self.recipients = None
        self.subject = None
        self.body = None
        self.attachments = None
        self.last_index = None

    def configure(self):
        pass

    def load(self):
        with open(self.RECIPIENTS_PATH) as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
        self.recipients = lines
        self.subject = self.open_and_read(self.SUBJECT_PATH)
        self.body = self.open_and_read(self.BODY_PATH)
        self.last_index = self.open_and_read(self.LAST_INDEX_PATH)
        try:
            self.last_index = int(self.last_index)
        except ValueError:
            self.last_index = 0
        self.attachments = glob.glob(os.path.join(self.ATTACHMENTS_PATH, '*'))

    def run(self):
        count = 0
        recipients = self.get_recipients()
        for recipient in recipients:
            try:
                self.create_and_send_email(recipient)
                count += 1
            except Exception as e:
                print(recipient)
                print(e)
        self.write_index_to_disk(recipients)
        return count

    def create_and_send_email(self, recipient):
        from django.core.mail import EmailMessage

        if isinstance(recipient, list):
            recipients = recipient
        else:
            recipients = [recipient]
        mail = EmailMessage(
            self.subject,
            self.body,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            recipients,
            reply_to=[settings.EMAIL_HOST_USER],
            # headers={'Message-ID': 'foo'},
        )
        for attachment in self.attachments:
            mail.attach(os.path.basename(attachment), open(attachment, 'rb').read())
        mail.send()

    def write_index_to_disk(self, recipients):
        curr_position = self.last_index + len(recipients)
        curr_index = curr_position if curr_position < len(self.recipients) else 0
        with open(self.LAST_INDEX_PATH, 'w') as f:
            f.write(str(curr_index))

    def get_recipients(self):
        if not self.last_index:
            recipients = self.recipients[:self.RECIPIENTS_PER_RUN]
        elif (self.last_index + self.RECIPIENTS_PER_RUN) > len(self.recipients):
            recipients = self.recipients[self.last_index:]
        else:
            recipients = self.recipients[self.last_index: self.last_index+self.RECIPIENTS_PER_RUN]
        return recipients

    @staticmethod
    def open_and_read(fname):
        with open(fname) as f:
            data = f.read().strip()
        return data


def run():
    m = Mailer()
    m.load()
    m.run()
