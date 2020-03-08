
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def setEmailAsHtml(self,toEmail,subject, htmlCotent):
        # po primeru iz: https://realpython.com/python-send-email/

        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = self.loginEmail
        msg['To'] = toEmail

        # Create the plain-text and HTML version of your message
        text = """\
        Zdravo,
        Vaš brskalnik ne dopušča html vsebine!
        """

        # html = """\
        # <html>
        # <body>
        #     <p>Hi,<br>
        #     How are you?<br>
        #     <a href="http://www.realpython.com">Real Python</a> 
        #     has many great tutorials.
        #     </p>
        # </body>
        # </html>
        # """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(htmlCotent, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        msg.attach(part1)
        msg.attach(part2)

        self.smtpServer.send_message(msg)
        self.smtpServer.quit()