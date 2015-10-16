# Copyright (C) 2015 Clemente Junior
#
# This file is part of SigeLib
#
# SigeLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.



import logging
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib

logging.basicConfig(filename='/home/dev/mail_bomber.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def send_image_mail(to, attachment_path, attachment_name, subject):
    """
Send a mail.
    :param to: mail recipients.
    :param attachment_path: attachment content.
    :param attachment_name: attachment name.
    :param subject: mail subject.
    """
    s = smtplib.SMTP(host='smtp.terra.com.br', port=587)
    msg = MIMEMultipart()
    file = open(attachment_path, 'rb')
    para_anexar = MIMEImage(file.read())
    para_anexar.add_header('Content-Disposition', 'attachment',
                           filename=attachment_name)
    msg['From'] = 'casanorteatacado@casanorte.com.br'
    if isinstance(to, (list, tuple)):
        msg['To'] = ', '.join(to)
    else:
        msg['To'] = to
    msg['Subject'] = subject
    msg.attach(para_anexar)
    try:
        s.login('casanorteatacado@casanorte.com.br', 'cnacpd')
        s.sendmail(msg['From'], msg['To'].split(', '), msg.as_string())
        s.quit()
        logging.info('msg sended to {}'.format(to))
    except Exception as err:
        msg_error = 'Erro ao enviar email {}\n{}'.format(msg[subject], err)
        logging.exception(msg_error)
        logging.exception(err)


if __name__ == '__main__':
    filer = open('/home/dev/emails.txt', 'r')
    emails = filer.readlines()
    filer.close()
    count = 0
    while count < 1000 and len(emails) > 0:
        send_image_mail(emails.pop(0).strip('\n'), '/home/dev/img.jpg',
                        'img.jpg',
                        'Informativos sobre fraudes em boletos bancários.')

        count += 1
        print(count)
    filew = open('/home/dev/emails.txt', 'w')
    filew.writelines(emails)
    filer.close()
