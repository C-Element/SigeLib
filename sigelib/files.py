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

import os
import tempfile
from datetime import datetime

from odf.style import Style, TableColumnProperties
from odf.text import P
from odf.table import Table, TableCell, TableColumn, TableRow
from odf.opendocument import OpenDocumentSpreadsheet


def generate_ods(data):
    """
    Generate a ODS file.
    :param data: list-like of dict with the data.
    :return:
    """
    doc = OpenDocumentSpreadsheet()
    table = Table()
    tr = TableRow()
    colautowidth = Style(name="co1", family="table-column")
    colautowidth.addElement(TableColumnProperties(useoptimalcolumnwidth=True))
    doc.automaticstyles.addElement(colautowidth)
    for column in data[0].keys():
        table.addElement(TableColumn(stylename=colautowidth))
        tc = TableCell(valuetype="string", value=column)
        tc.addElement(P(text=column))
        tr.addElement(tc)
    table.addElement(tr)
    for row in data:
        tr = TableRow()
        for column in row.keys():
            tc = TableCell(valuetype="string", value=row[column])
            tc.addElement(P(text=row[column]))
            tr.addElement(tc)
        table.addElement(tr)
    file = os.path.join(tempfile.gettempdir(), 'SIGE' +
                        datetime.now().strftime('%Y%m%d%H%M%S%f') + '.ods')
    doc.spreadsheet.addElement(table)
    print(doc.automaticstyles.childNodes[0].attributes)
    doc.save(file)
    return file
