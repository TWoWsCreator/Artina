import email.mime.text
import logging
import smtplib

import django.conf


def searching_paintings(paintings, result_search):
    if result_search:
        try:
            return (
                paintings.filter(painting_creation_year=result_search)
                | paintings.filter(painting_size__iregex=result_search)
                | paintings.filter(painting_description__iregex=result_search)
            )
        except ValueError:
            return (
                paintings.filter(painting_description__iregex=result_search)
                | paintings.filter(painting_size__iregex=result_search)
                | paintings.filter(painting_name__iregex=result_search)
                | paintings.filter(
                    painting_gallery__gallery_name__iregex=result_search
                )
            )
    else:
        return paintings


def send_mail_user(msg, to_mail, msg_subj):
    password = django.conf.settings.SMTP_KEY
    from_mail = django.conf.settings.APP_MAIL
    server = smtplib.SMTP(django.conf.settings.SMTP_MAIL, port=587)
    server.starttls()
    print(from_mail, password)
    server.login(from_mail, password)
    msg = email.mime.text.MIMEText(msg)
    msg['Subject'] = msg_subj

    try:
        server.sendmail(from_mail, to_mail, msg.as_string())
    except Exception as err:
        logging.error(err)
