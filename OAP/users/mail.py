import smtplib
from email.mime.text import MIMEText


# from apscheduler.schedulers.blocking import BlockingScheduler


def sendEmail(touser, msg):
    host = 'smtp.gmail.com:587'
    fromuser = ''
    pasword = ''
    body = '<h1>' + "You have an appointment within 24 hours, please check it. <From Tom Grooming Company.>" + '</h1>' + '<p>' + msg + '</p>'
    msg = MIMEText(body, 'html')
    msg['subject'] = 'A reminder for your grooming appointment'
    msg['from'] = fromuser
    server = smtplib.SMTP(host)
    server.starttls()
    server.login(fromuser, pasword)
    msg['to'] = touser
    server.sendmail(fromuser, touser, msg.as_string())


def sendSuccessEmail(touser, msg):
    host = 'smtp.gmail.com:587'
    fromuser = ''
    pasword = ''
    body = '<h1>' + 'Detail of your appointment:' + '</h1>' + '<p>' + msg + '</p>'
    msg = MIMEText(body, 'html')
    msg['subject'] = "You have booked successfully. <From Tom Grooming Company.>"
    msg['from'] = fromuser
    server = smtplib.SMTP(host)
    server.starttls()
    server.login(fromuser, pasword)
    msg['to'] = touser
    server.sendmail(fromuser, touser, msg.as_string())


def main():
    sendEmail()


if __name__ == '__main__':
    main()
