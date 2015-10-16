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


from datetime import date, time

from sigelib.utils import fill_with


def CEP(text):
    """
    Format to display CEP fields
    :param text:
    :return:
    """
    if not isinstance(text, str):
        text = str(text)
    text = fill_with(text, '0', 8)
    return '{}.{}-{}'.format(text[0:2], text[2:5], text[5:])


def CURRENCY(text):
    """
    Format to display currency fields
    :param text:
    :return:
    """
    if not isinstance(text, str):
        text = str(text)
    digits = text.split('.')
    to_return = ''
    counter = 0
    integer = digits[0]
    decimal = '00' if len(digits) == 1 else fill_with(digits[1], '0', 2, True)
    for i in integer[::-1]:
        if counter > 0 and counter % 3 == 0:
            to_return = '.' + to_return
        to_return = i + to_return
        counter += 1
    return 'R$ {},{}'.format(to_return, decimal)


def CNPJ(text):
    """
    Format to display CNPJ fields
    :param text:
    :return:
    """
    if not isinstance(text, str):
        text = str(text)
    text = fill_with(text, '0', 14)
    return '{}.{}.{}/{}-{}'.format(text[0:2], text[2:5], text[5:8], text[8:12],
                                   text[12:])


def CPF(text):
    """
    Format to display CPF fields
    :param text:
    :return:
    """
    if not isinstance(text, str):
        text = str(text)
    text = fill_with(text, '0', 11)
    return '{}.{}.{}-{}'.format(text[0:3], text[3:6], text[6:9], text[9:])


def DATE(value):
    """
    Format to display date fields
    :param text:
    :return:
    """
    if not isinstance(value, date):
        raise ValueError('Can\'t convert ({}){} to date'.format(type(value),
                                                                value))
    return value.strftime('%d/%m/%Y')


def DATETIME(value):
    """
    Format to display datetime fields
    :param text:
    :return:
    """
    if not isinstance(value, date):
        raise ValueError(
            'Can\'t convert ({}){} to datetime'.format(type(value), value))
    return value.strftime('%d/%m/%Y %H:%S')


def PHONE(text):
    """
    Format to display phone fields
    :param text:
    :return:
    """
    if not isinstance(text, str):
        text = str(text)
    if len(text) in (8, 9):
        return '(  ) {}-{}'.format(text[0:5], text[5:])
    elif len(text) in (10, 11):
        return '({}) {}-{}'.format(text[0:2], text[2:7], text[7:])
    else:
        text = fill_with(text, '0', 8)
        return '(  ) {}-{}'.format(text[0:5], text[5:8])


def TIME(value):
    """
    Format to display time fields
    :param text:
    :return:
    """
    if not isinstance(value, time):
        raise ValueError('Can\'t convert ({}){} to time'.format(type(value),
                                                                value))
    return value.strftime('%H:%S')
