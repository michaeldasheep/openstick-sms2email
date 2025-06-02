import smtplib
import ssl
import config

def sendEmail(messagePARSED):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.SERVER, config.PORT, context=context) as smtp:
        smtp.login(config.USERNAME, config.PASSWORD)
        smtp.sendmail(config.USERNAME, config.RECIPIENT, messagePARSED.as_string())
        smtp.quit()

