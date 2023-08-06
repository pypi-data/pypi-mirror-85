import smtplib
from email.mime.text import MIMEText


def sendmail(IP, Subject, From, To):
    """

    :param IP: SMTP地址
    :param Subject: 标题
    :param From: 发送方 dawei
    :param To: 接收方 123123123@qq.com
    :return:
    """
    msg = MIMEText(Subject)
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To
    s = smtplib.SMTP(IP)
    s.send_message(msg)
    s.quit()
