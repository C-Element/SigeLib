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


from datetime import time, timedelta, date, datetime
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import sha256
import smtplib
import calendar

from sigelib.consts import FPP_XMPP_RECIPIENTS, NORMAL_XMPP_RECIPIENTS, \
    GLEYBER_XMPP_RECIPIENT, GLEYBER_MAIL_RECIPIENT, MANAGERS_MAIL_RECIPIENT, \
    MANAGERS_XMPP_RECIPIENT
from sigelib.xmpp_ponto import XMPPPonto

T_NONE = type(None)
DEFAULT_PASSWORD = sha256(b'padrao').hexdigest()
IMG_PREAMBLE = b'data:image/png;base64,'


def all_as_str(obj, fdate='%d/%m/%Y', fdatetime='%d/%m/%Y %H:%S',
               ftime='%d/%m/%Y %H:%S'):
    """
    Return all values from the list-like or dict object.
    """
    to_return = []
    if isinstance(obj, dict):
        to_return = {}
        for key in obj:
            if isinstance(obj[key], datetime):
                to_return[key] = obj[key].strftime(fdatetime)
            elif isinstance(obj[key], date):
                to_return[key] = obj[key].strftime(fdate)
            elif isinstance(obj[key], time):
                to_return[key] = obj[key].strftime(ftime)
            elif isinstance(obj[key], str):
                to_return[key] = obj[key]
            elif obj[key] is None:
                to_return[key] = ''
            else:
                to_return[key] = str(obj[key])
    else:
        for data in obj:
            if isinstance(data, datetime):
                to_return.append(data.strftime(fdatetime))
            elif isinstance(data, date):
                to_return.append(data.strftime(fdate))
            elif isinstance(data, time):
                to_return.append(data.strftime(ftime))
            elif isinstance(data, str):
                to_return.append(data)
            elif data is None:
                to_return.append('')
            else:
                to_return.append(str(data))
    return to_return


def can_be_numeric(value):
    """
Return true if value can be a number.
    :param value: The object to be evalueted.
    :return: True if the object can be a number, else False
    """
    try:
        float(value)
        return True
    except:
        return False


def if_not_time(time_to_eval, if_not, as_string=True):
    """
Retur the if_not object if time_to_eval isn't instance of time.
    :param time_to_eval: object to eval is a time.
    :param if_not: object to be returned.
    :param as_string: is the time is to be returned as string.
    :return: time_to_eval if it's a instance of time, else if_not.
    """
    if isinstance(time_to_eval, time):
        if as_string:
            return time_to_eval.strftime("%H:%M")
        else:
            return time_to_eval
    else:
        return if_not


def fill_with(obj, char, size, at_end=False):
    """
Fill obj with char, and return a string.
    :param obj: object to be filled.
    :param char: char to fill blank spaces.
    :param size: size of desired string.
    :param at_end: if will insert char at the end, otherwise will be isnert at
                   the start.
    :return: a new string of desired size.
    """
    if not isinstance(obj, str):
        obj = str(obj)
    length = len(obj)
    need = size - length
    if need <= 0:
        return obj[0:size]
    if at_end:
        return obj + char * need
    else:
        return char * need + obj


def join_br(frst_part, scnd_part):
    """
Join two string with a <br> tag.
    :param frst_part: first part of the string.
    :param scnd_part: second part of the string.
    :return: a new string as 'frst_part<br>scndr_part'.
    """
    if isinstance(frst_part, T_NONE) or frst_part == '':
        return scnd_part
    else:
        return frst_part + '<br>' + scnd_part


def load_decimal(value):
    """
    Load decimal values
    :param value:
    :return:
    """
    if value:
        return Decimal(value)
    return None


def load_date(value, fmt='%d/%m/%Y'):
    """
    Load date values
    """
    if value:
        return datetime.strptime(value, fmt).date()
    return None


def load_int(value):
    """
    Load int values
    """

    if value:
        new_str = ''
        for char in value:
            if can_be_numeric(char):
                new_str += char
        return int(new_str)
    return None


def load_int_as_str(value):
    """
    Load int values as string.
    """

    if value:
        new_str = ''
        for char in value:
            if can_be_numeric(char):
                new_str += char
        return new_str
    else:
        return None


def load_time(value, fmt='%H:%M'):
    """
    Load time values
    """

    if value:
        return datetime.strptime(value, fmt).time()
    return None


def send_clemente_xmpp_message(message):
    """
Send a XMPP message for clemente user.
    :param message: Message to be sended.
    """
    send_xmpp_message(['clemente@casanorte.vpn'], message)


def send_fpp_xmpp_message(message):
    """
Send a XMPP message for FPP'a users.
    :param message: Message to be sended.
    """
    send_xmpp_message(FPP_XMPP_RECIPIENTS, message)


def send_gleyber_mail(attachment_content, attachment_name, subject):
    """
Send a mail for gleyber user.
    :param attachment_content: attachment content.
    :param attachment_name: attachment name.
    :param subject: mail subject.
    """
    send_mail(GLEYBER_MAIL_RECIPIENT, attachment_content, attachment_name,
              subject)


def send_gleyber_xmpp_message(message):
    """
Send a XMPP message for gleyber user.
    :param message: Message to be sended.
    """
    send_xmpp_message(GLEYBER_XMPP_RECIPIENT, message)


def send_mail(to, attachment_content, attachment_name, subject):
    """
Send a mail.
    :param to: mail recipients.
    :param attachment_content: attachment content.
    :param attachment_name: attachment name.
    :param subject: mail subject.
    """
    s = smtplib.SMTP(host='smtp.terra.com.br', port=587)
    msg = MIMEMultipart()
    para_anexar = MIMEText(attachment_content, _subtype='vnd.ms-excel',
                           _charset='cp1252')
    para_anexar.add_header('Content-Disposition', 'attachment',
                           filename=attachment_name)
    msg['From'] = 'cpd@casanorte.com.br'
    msg['To'] = ', '.join(to)
    msg['Subject'] = subject
    msg.attach(para_anexar)
    try:
        s.login('cpd@casanorte.com.br', 'ultrium')
        s.sendmail(msg['From'], msg['To'].split(', '), msg.as_string())
        s.quit()
    except Exception as err:
        msg_error = 'Erro ao enviar email {}\n{}'.format(msg[subject], err)
        print(msg_error)
        print(err)
        send_clemente_xmpp_message(msg_error)


def send_managers_mail(attachment_content, attachment_name, subject):
    """
Send a mail for manager's user.
    :param attachment_content: attachment content.
    :param attachment_name: attachment name.
    :param subject: mail subject.
    """
    send_mail(MANAGERS_MAIL_RECIPIENT, attachment_content, attachment_name,
              subject)


def send_managers_xmpp_message(message):
    """
Send a XMPP message for all managers.
    :param message: Message to be sended.
    """
    send_xmpp_message(MANAGERS_XMPP_RECIPIENT, message)


def send_normal_xmpp_message(message):
    """
Send a XMPP message for normal users.
    :param message: Message to be sended.
    """
    send_xmpp_message(NORMAL_XMPP_RECIPIENTS, message)


def send_xmpp_message(recipients, message):
    """
Send a XMPP message.
    :param recipients: message recipients.
    :param message: message to be sended.
    """
    xmpp = XMPPPonto('sige@casanorte.vpn', 'r31@rthur',
                     recipients, message)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0199')
    if xmpp.connect(('10.10.1.86', 5222), use_ssl=False):
        xmpp.process(block=True)
        if not recipients:
            print('sem destinatários')
    else:
        print("Unable to connect(1).\n" + message)


def time_between_10_120(time_to_eval):
    """
Verify if the time_to_eval is between 1H15Min and 2H05Min.
    :param time_to_eval: time to be evalueted.
    :return: The time interval if the the time is in this interval, else None.
    """
    to_return = None
    if time(0, 10) <= time_to_eval < time(0, 20):
        to_return = time(0, 10)
    elif time(0, 20) <= time_to_eval < time(0, 30):
        to_return = time(0, 20)
    elif time(0, 30) <= time_to_eval < time(0, 40):
        to_return = time(0, 30)
    elif time(0, 40) <= time_to_eval < time(0, 50):
        to_return = time(0, 40)
    elif time(0, 50) <= time_to_eval < time(1, 0):
        to_return = time(0, 50)
    elif time(1, 0) <= time_to_eval < time(1, 10):
        to_return = time(1, 0)
    elif time(1, 10) <= time_to_eval < time(1, 20):
        to_return = time(1, 10)
    elif time(1, 20) <= time_to_eval < time(1, 30):
        to_return = time(1, 20)
    return to_return


def time_between_115_205(time_to_eval):
    """
Verify if the time_to_eval is between 1H15Min and 2H05Min.
    :param time_to_eval: time to be evalueted.
    :return: The time interval if the the time is in this interval, else None.
    """
    to_return = None
    if time(1, 15) <= time_to_eval < time(1, 30):
        to_return = time(1, 15)
    elif time(1, 30) <= time_to_eval < time(1, 35):
        to_return = time(1, 30)
    elif time(1, 35) <= time_to_eval < time(1, 40):
        to_return = time(1, 35)
    elif time(1, 40) <= time_to_eval < time(1, 45):
        to_return = time(1, 40)
    elif time(1, 45) <= time_to_eval < time(1, 50):
        to_return = time(1, 45)
    elif time(1, 50) <= time_to_eval < time(1, 55):
        to_return = time(1, 50)
    elif time(1, 55) <= time_to_eval < time(2):
        to_return = time(1, 55)
    elif time(2) <= time_to_eval < time(2, 5):
        to_return = time(2)
    elif time(2, 5) >= time_to_eval:
        to_return = time(2, 5)
    return to_return


def time_between_430_610(time_to_eval):
    """
Verify if the time_to_eval is between 4H30Min and 6H10Min.
    :param time_to_eval: time to be evalueted.
    :return: The time interval if the the time is in this interval, else None.
    """
    to_return = None
    if time(4, 30) <= time_to_eval < time(4, 40):
        to_return = time(4, 30)
    elif time(4, 40) <= time_to_eval < time(4, 50):
        to_return = time(4, 40)
    elif time(4, 50) <= time_to_eval < time(5):
        to_return = time(4, 50)
    elif time(5) <= time_to_eval < time(5, 10):
        to_return = time(5)
    elif time(5, 10) <= time_to_eval < time(5, 20):
        to_return = time(5, 10)
    elif time(5, 20) <= time_to_eval < time(5, 30):
        to_return = time(5, 20)
    elif time(5, 30) <= time_to_eval < time(5, 40):
        to_return = time(5, 30)
    elif time(5, 40) <= time_to_eval < time(5, 50):
        to_return = time(5, 40)
    elif time(5, 50) <= time_to_eval < time(6):
        to_return = time(5, 50)
    elif time(6) <= time_to_eval < time(6, 10):
        to_return = time(6)
    elif time(6, 10) <= time_to_eval:
        to_return = time(6, 10)
    return to_return


class HDateTime:
    """
    Old class to manipulate datetime objects... used into any functions on
    SigeLib, but has a long time that the code isn't
    """

    @staticmethod
    def first_day(month=None, year=None, the_date=None):
        """
Return the first day of month of the given date.
        :param month:
        :param year:
        :param the_date:
        :return:
        """
        if the_date:
            return date(the_date.year, the_date.month, 1)
        elif month and year:
            return date(year, month, 1)
        else:
            return HDateTime.first_day(the_date=HDateTime.today())

    @staticmethod
    def last_day(month=None, year=None, the_date=None):
        """
Return the last day of month of the given date.
        :param month:
        :param year:
        :param the_date:
        :return:
        """
        if the_date:
            return date(the_date.year, the_date.month,
                        calendar.monthrange(the_date.year, the_date.month)[1])
        elif month and year:
            return date(year, month, calendar.monthrange(year, month)[1])
        else:
            return HDateTime.last_day(the_date=HDateTime.today())

    @staticmethod
    def calc_days(the_date, days):
        """
Return a date addeed the days at the_date.
        :param the_date:
        :param days:
        :return:
        """
        delta_days = timedelta(days=days)
        return the_date + delta_days

    @staticmethod
    def dif_time(the_time, other_time):
        if the_time < other_time:
            result = HDateTime.dif_time(time(23, 59, 59), other_time)
            result2 = HDateTime.dif_time(the_time, time())
            return HDateTime.sum_times(
                HDateTime.sum_times(result, time(0, 0, 1)), result2)
        else:
            total_hours = the_time.hour - other_time.hour
            total_minutes = 60 + the_time.minute - other_time.minute
            total_seconds = 60 + the_time.second - other_time.second
            if total_seconds >= 60:
                total_seconds -= 60
            else:
                total_minutes -= 1
            if total_minutes >= 60:
                total_minutes -= 60
            else:
                total_hours -= 1
            return time(total_hours, total_minutes, total_seconds)

    @staticmethod
    def sum_times(the_time, other_time):
        total_seconds = the_time.second + other_time.second
        total_minutes = the_time.minute + other_time.minute
        total_hours = the_time.hour + other_time.hour
        if total_seconds >= 60:
            total_minutes += 1
            total_seconds -= 60
        if total_minutes >= 60:
            total_hours += 1
            total_minutes -= 60
        if total_hours >= 24:
            total_hours -= 24
        return time(total_hours, total_minutes, total_seconds)

    @staticmethod
    def calc_hours(the_time, amount):
        """
Calculate Hours.
        :param the_time: tuple formatted as (int(hours), int(minutes))
        :param amount: tuple formatted as (int(hours), int(minutes)) to be
        added to the_time
        :return: tuple formatted as (int(hours), int(minutes)) of the_time +
        amount
        """
        the_date = datetime.combine(date.today(), the_time) + timedelta(
            hours=amount)
        if the_date.date() == date.today():
            return the_date.time().hour, the_date.time().minute
        if the_date.date() - date.today():
            return the_date.time().hour, the_date.time().minute
        days = the_date.date() - date.today()

    @staticmethod
    def today():
        return date.today()

    @staticmethod
    def time_now():
        return datetime.now().time()

    @staticmethod
    def to_db(the_date):
        return the_date.strftime('%d-%b-%Y')

    @staticmethod
    def get_time_from_str(string):
        """

        :param string:
        :return:
        """
        formated = string.replace('.', ':').split(':')
        return time(int(formated[0]), int(formated[1]),
                    (int(formated[2]) if len(formated) > 2 else 0),
                    (int(formated[3]) if len(formated) > 3 else 0))

    @staticmethod
    def timefsecs(secs):
        """
        Return time object from secs
        :param secs:
        :return:
        """
        tmp = HDateTime.total_hours_from_seconds(secs)
        return time(tmp[0], tmp[1], tmp[2])

    @staticmethod
    def total_hours_from_seconds(secs):
        """
        Get [Hours, Minutes, Seconds] from secs
        :param secs:
        :return:
        """
        hours = int(secs / 3600)
        minutes = int((secs % 3600) / 60)
        seconds = int(secs % 60)
        return hours, minutes, seconds

    @staticmethod
    def amount_hours(*times):
        total_sec = 0
        for t in times:
            total_sec += 60 * 60 * t.hour
            total_sec += 60 * t.minute
            total_sec += t.second
        return HDateTime.total_hours_from_seconds(total_sec)
