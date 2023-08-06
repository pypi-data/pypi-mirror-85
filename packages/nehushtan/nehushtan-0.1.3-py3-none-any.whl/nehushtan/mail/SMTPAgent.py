#  Copyright (c) 2020. Sinri Edogawa

import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from typing import Iterable


class SMTPAgent:
    __smtp_server: str
    __smtp_port: int

    __password: str

    _sender: str
    _receivers: Iterable[str]
    _subject: str
    _content: str
    _attachments: Iterable[str]

    def __init__(self, sender: str, password: str, smtp_server: str, smtp_port: int):
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self._sender = sender
        self.__password = password

        self._receivers = []
        self._subject = ''
        self._content = ''
        self._attachments = []

    def set_receivers(self, receivers: Iterable[str]):
        self._receivers = receivers
        return self

    def set_subject(self, subject: str):
        self._subject = subject
        return self

    def set_content(self, content: str):
        self._content = content
        return self

    def set_attachments(self, attachments: Iterable[str]):
        self._attachments = attachments
        return self

    @staticmethod
    def _format_address(s):
        name, addr = parseaddr(s)
        return formataddr(
            (
                Header(name, 'utf-8').encode(),
                addr
            )
        )

    def send(self):
        message_html = MIMEMultipart()
        message_html['From'] = self._format_address(self._sender)

        to_list = []
        for receiver in self._receivers:
            to_list.append(self._format_address(receiver))

        message_html['To'] = ','.join(to_list)

        message_html['Subject'] = Header(self._subject, 'gbk')
        message_html.attach(MIMEText(self._content, 'html', 'utf-8'))

        for attachment in self._attachments:
            file_name = os.path.basename(attachment)
            part = MIMEApplication(open(attachment, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=file_name)  # 给附件重命名,一般和原文件名一样,改错了可能无法打开.
            message_html.attach(part)

        server = smtplib.SMTP_SSL(self.__smtp_server, self.__smtp_port)
        server.login(self._sender, self.__password)
        server.sendmail(self._sender, self._receivers, message_html.as_string())
        server.quit()

        return self
