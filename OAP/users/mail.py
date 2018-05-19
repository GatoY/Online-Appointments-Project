import smtplib
# from forex_python.converter import CurrencyRates
from email.mime.text import MIMEText
# from apscheduler.schedulers.blocking import BlockingScheduler


def sendEmail(touser):
    # receiver = CurrencyRates()
    # CNY2AUD = receiver.get_rate('AUD', 'CNY')
    host = 'smtp.gmail.com:587'
    fromuser = ''
    pasword = 'Lostwechat170921'
    # touser = 'derakhy@gmail.com'
    body = '<h1>' + "You have an appointment within 24 hours, please check it. <From Tom Grooming Company.>" + '</h1>'
    # body = '<h1>' + str(CNY2AUD) + '</h1>'
    msg = MIMEText(body, 'html')
    msg['subject'] = 'A reminder for your grooming appointment'
    msg['from'] = fromuser
    # msg['to'] = touser
    server = smtplib.SMTP(host)
    server.starttls()
    server.login(fromuser, pasword)
    msg['to'] = touser
    server.sendmail(fromuser, touser, msg.as_string())
def main():
    sendEmail()

if __name__== '__main__':
    main()

# print ' over'
# scheduler = BlockingScheduler()
# scheduler.add_job(sendEmail, 'cron', day_of_week='1-7', hour=10, minute=30)
# scheduler.start()
