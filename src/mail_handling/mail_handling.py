print('In File: src/mail_handling/mail_handling.py')

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configs import mail_config


def read_template(filename):
    print('In Method: read_template()')
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_confirmation_mail(name: str, email: str):
    print('In Method: send_mail()')

    message_template = read_template('templates/emails/confirmation_mail.txt')

    try:
        # set up the SMTP server
        s = smtplib.SMTP(host='mail.privateemail.com', port=587)
        s.starttls()
        s.login(mail_config.address, mail_config.password)

        # For each contact, send the email:
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name)

        # setup the parameters of the message
        msg['From'] = 'info@kurzegeschichte.de'
        msg['To'] = email
        msg['Subject'] = "Bestätige deine Registrierung bei kurzegeschichte."

        # add in the message body
        msg.attach(MIMEText(message, 'html'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

        # Terminate the SMTP session and close the connection
        s.quit()
    except smtplib.SMTPException as e:
        print(e)

    return True
