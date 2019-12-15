
import smtplib
from email.message import EmailMessage

class Email:
    def __init__(self):
        self.loginEmail = "jan.cvek@gmail.com"
        self.loginPass = "dajko-E1"

        self.loginToSmtp()

    def loginToSmtp(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(self.loginEmail, self.loginPass)

        self.smtpServer = server

    def sentEmail(self,toEmail,subject, content):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.loginEmail
        msg['To'] = toEmail
        msg.set_content(content)

        self.smtpServer.send_message(msg)
        self.smtpServer.quit()