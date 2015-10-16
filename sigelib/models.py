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


from base64 import b64decode
from datetime import datetime
from hashlib import sha256
import json
import sys

from werkzeug.exceptions import BadRequestKeyError, abort

from sigelib.formats import DATE, PHONE, CPF, CEP, CURRENCY, CNPJ, DATETIME, \
    TIME
from sigelib.utils import load_date, load_int, load_int_as_str, load_decimal, \
    load_time, all_as_str
from sigelib.connections import create_sige, create_mss_inner, \
    create_mss_gate, create_mss_driver, create_mss_top, create_oracle

sys.path.append('../BifrostDB/')

from bifrost.utils import nwe, replace_when_none
from bifrost.db import Query

from bifrost.models import BaseModel, CharField, IntField, BoolField, \
    ForeignField, DateField, BytesField, DecimalField, TimeField, DateTimeField

T_DICT = 'dict'


class Access(BaseModel):
    choices = (0, 1, 2)

    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_access'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.admin = BoolField(default_value=False)
        self.access_control = IntField(default_value=0, choices=self.choices)
        self.curricula = IntField(default_value=0, choices=self.choices)
        self.departments = IntField(default_value=0, choices=self.choices)
        self.disciplinary_sanctions = IntField(default_value=0,
                                               choices=self.choices)
        self.employees = IntField(default_value=0, choices=self.choices)
        self.enterprises = IntField(default_value=0, choices=self.choices)
        self.roles = IntField(default_value=0, choices=self.choices)
        self.salary = IntField(default_value=0, choices=self.choices)
        self.users = IntField(default_value=0, choices=self.choices)
        self.reports = CharField(null=True, default_value=None)
        self.widgets = CharField(null=True, default_value=None)
        self.bf_prepare()

    def widgets_list(self, to_add=None, to_del=None):
        if self.widgets:
            data = self.widgets.split(', ')
        else:
            data = []
        if to_add:
            data.append(to_add)
        elif to_del:
            if to_del in data:
                data.remove(to_del)
        else:
            return tuple(data)
        self.widgets = ', '.join(data)

    def reports_list(self, to_add=None, to_del=None):
        if self.reports:
            data = self.reports.split(', ')
        else:
            data = []
        if to_add:
            data.append(to_add)
        elif to_del:
            if to_del in data:
                data.remove(to_del)
        else:
            return tuple(data)
        self.reports = ', '.join(data)

    def load_from_web(self, form):
        try:
            self.access_control = int(form['access_control'])
            self.curricula = int(form['curricula'])
            self.departments = int(form['departments'])
            self.disciplinary_sanctions = int(form['disciplinary_sanctions'])
            self.employees = int(form['employees'])
            self.enterprises = int(form['enterprises'])
            self.roles = int(form['roles'])
            self.salary = int(form['salary'])
            self.users = int(form['users'])
            if 'is_admin' in form:
                self.admin = True
            else:
                self.admin = False
        except BadRequestKeyError:
            abort(403)


class Aso(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_asos'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.date = DateField(display=DATE)
        self.type = CharField()
        self.employee = ForeignField(Employee, field_name='eid')
        self.document = BytesField(null=True)
        self.document_ext = CharField(max_length=5, null=True)
        self.conclusion = BoolField(default_value=True)
        self.observations = CharField(max_length=1024, null=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.date = load_date(form['date'])
            self.type = nwe(form['type'])
            self.conclusion = form['conclusion'] == 'Y'
            self.observations = nwe(form['observations'])
            self.document_ext = replace_when_none(
                nwe(form['document_filename'].split('.')[-1]),
                self.document_ext)
            if len(form['document']) > 0:
                self.document = b64decode(
                    form['document'].split(';base64,')[1].encode())
        except BadRequestKeyError as ke:
            abort(403)


class Department(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_departments'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.name = CharField(max_length=100)
        self.active = BoolField(default_value=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.name = form['name']
            self.active = 'active' in form
        except BadRequestKeyError:
            abort(403)


class Dependent(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_dependents'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.name = CharField()
        self.born_date = DateField(display=DATE)
        self.kinship = CharField()
        self.employee = ForeignField(Employee, field_name='eid')
        self.active = BoolField(default_value=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.name = form['name']
            self.born_date = load_date(form['born_date'])
            self.kinship = form['kinship']
        except BadRequestKeyError:
            abort(403)


class DisciplinarySanction(BaseModel):
    type_choices = {1: 'Advertência', 2: '>Justa Causa', 3: 'Suspensão',
                    4: 'Termo de Ciência'}
    reason_choices = {1: 'ABANDONO DE EMPREGO', 2: 'ATO DE IMPROBIDADE',
                      3: 'ATO DE INDISCIPLINA OU DE INSUBORDINAÇÃO',
                      4: 'ATO LESIVO CONTRA EMPREGADOR E SUPERIOR',
                      5: 'ATO LESIVO CONTRA QUALQUER PESSOA',
                      6: 'CONDENAÇÃO CRIMINAL',
                      7: 'DESÍDIA NO DESEMP. DAS RESPEC. FUNÇÕES',
                      8: 'EMBRIAGUEZ HABITUAL OU EM SERVIÇO',
                      9: 'INCONT. DE CONDUTA OU MAU PROCEDIM.',
                      10: 'NEGOCIAÇÃO HABITUAL',
                      11: 'PRÁTICA CONSTANTE DE JOGOS DE AZAR',
                      12: 'VIOLAÇÃO DE SEGREDO DA EMPRESA'}

    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_disciplinary_sanctions'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.employee = ForeignField(Employee, field_name='eid')
        self.type = IntField(choices=self.type_choices, default_value=1)
        self.date = DateField(display=DATE)
        self.reason = IntField(choices=self.reason_choices, default_value=1)
        self.requester = CharField()
        self.witness1 = CharField(null=True)
        self.witness2 = CharField(null=True)
        self.observations = CharField(null=True)
        self.document = BytesField(null=True)
        self.document_ext = CharField(null=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.type = int(form['type'])
            self.date = load_date(form['date'])
            self.reason = int(form['reason'])
            self.requester = form['requester']
            self.witness1 = nwe(form['witness1'])
            self.witness2 = nwe(form['witness2'])
            self.observations = nwe(form['observations'])
            self.document_ext = replace_when_none(
                nwe(form['document_filename'].split('.')[-1]),
                self.document_ext)
            if len(form['document']) > 0:
                self.document = b64decode(
                    form['document'].split(';base64,')[1].encode())
        except BadRequestKeyError:
            abort(403)

    @property
    def reason_text(self):
        return self.reason_choices[self.type]

    @property
    def type_text(self):
        return self.type_choices[self.type]


class Employee(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_Employees'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.account = CharField(null=True, max_length=10)
        self.active = BoolField(default_value=True)
        self.address = CharField(null=True, max_length=150)
        self.address_adjunct = CharField(null=True, max_length=150)
        self.admission_date = DateField(display=DATE)
        self.agency = CharField(null=True, max_length=10)
        self.bank = CharField(null=True, max_length=50)
        self.born_date = DateField(null=True, display=DATE)
        self.cellphone = CharField(null=True, max_length=13, display=PHONE)
        self.city = CharField(null=True, max_length=50)
        self.civil_state = CharField(default_value='S', max_length=1)
        self.cnh = CharField(null=True, max_length=20)
        self.cnh_category = CharField(null=True, max_length=10)
        self.cpf = IntField(display=CPF)
        self.ctps = CharField(null=True, max_length=15)
        self.ctps_date = DateField(null=True, display=DATE)
        self.ctps_fu = CharField(null=True, max_length=2)
        self.ctps_series = CharField(null=True, max_length=10)
        self.demission_date = DateField(null=True, display=DATE)
        self.department = ForeignField(Department)
        self.enterprise = ForeignField(Enterprise)
        self.father_name = CharField(null=True, max_length=100)
        self.fu = CharField(null=True, max_length=2)
        self.graduation = CharField(null=True)
        self.meal_on_enterprise = BoolField(default_value=False)
        self.mother_name = CharField(null=True, max_length=100)
        self.nacionality = CharField(null=True, max_length=55)
        self.name = CharField(max_length=100)
        self.name_tag = IntField(null=True)
        self.neighborhood = CharField(null=True, max_length=50)
        self.phone = CharField(null=True, max_length=13, display=PHONE)
        self.photo = BytesField(null=True)
        self.pis_date = DateField(null=True, display=DATE)
        self.pis_number = IntField()
        self.place_of_birth = CharField(null=True, max_length=55)
        self.post_graduation = CharField(null=True)
        self.registry = IntField()
        self.reservist = CharField(null=True, max_length=30)
        self.rg = CharField(null=True, max_length=12, )
        self.rg_date = DateField(null=True, display=DATE)
        self.rg_issuing = CharField(null=True, max_length=10)
        self.role = ForeignField(Role)
        self.salary = DecimalField(null=True, display=CURRENCY)
        self.scholarity = IntField(null=True)
        self.scholarity_complete = BoolField(default_value=False)
        self.sex = CharField(default_value='M', max_length=1)
        self.spouse = CharField(null=True, max_length=100)
        self.transport_voucher = BoolField(default_value=False)
        self.winthor_registry = IntField(null=True)
        self.zipcode = IntField(null=True, display=CEP)
        self.bf_prepare()

    def load_from_web(self, form, files):
        try:
            self.department = Department()
            self.enterprise = Enterprise()
            self.role = Role()

            self.name = form['name']
            self.department.load(int(form['departament']))
            self.enterprise.load(int(form['enterprise']))
            self.role.load(int(form['role']))
            self.registry = load_int(form['registry'])
            self.name_tag = load_int(form['name_tag'])
            self.active = form['active'] == 'Y'
            self.cpf = load_int(form['cpf'])
            self.sex = nwe(form['sex'])
            self.rg = nwe(form['rg'])
            self.rg_issuing = nwe(form['rg_issuing'])
            self.rg_date = nwe(form['rg_date'])
            self.born_date = load_date(form['born_date'])
            self.cnh = nwe(form['cnh'])
            self.cnh_category = nwe(form['cnh_category'])
            self.ctps = nwe(form['ctps'])
            self.ctps_series = nwe(form['ctps_series'])
            self.ctps_fu = nwe(form['ctps_fu'])
            self.ctps_date = nwe(form['ctps_date'])
            self.nacionality = nwe(form['nacionality'])
            self.place_of_birth = nwe(form['place_of_birth'])
            self.phone = load_int_as_str(form['phone'])
            self.cellphone = load_int_as_str(form['cellphone'])
            self.zipcode = load_int_as_str(form['zipcode'])
            self.address = nwe(form['address'])
            self.address_adjunct = nwe(form['address_adjunct'])
            self.neighborhood = nwe(form['neighborhood'])
            self.city = nwe(form['city'])
            self.fu = nwe(form['fu'])
            self.father_name = nwe(form['father_name'])
            self.mother_name = nwe(form['mother_name'])
            self.scholarity = load_int(form['scholarity'])
            self.scholarity_complete = form['scholarity_complete'] == 'Y'
            self.graduation = nwe(form['graduation'])
            self.post_graduation = nwe(form['post_graduation'])
            self.civil_state = nwe(form['civil_state'])
            self.spouse = nwe(form['spouse'])
            self.admission_date = load_date(form['admission_date'])
            self.demission_date = load_date(form['demission_date'])
            self.pis_date = load_date(form['pis_date'])
            self.pis_number = load_int(form['pis_number'])
            self.meal_on_enterprise = form['meal_on_enterprise'] == 'Y'
            self.salary = load_decimal(form['salary'])
            self.reservist = nwe(form['reservist'])
            self.bank = nwe(form['bank'])
            self.agency = nwe(form['agency'])
            self.account = nwe(form['account'])
            self.winthor_registry = load_int(form['winthor_registry'])
            self.transport_voucher = form['transport_voucher'] == 'Y'
            data = files['photo'].stream.read()
            if data != b'':
                self.photo = data
        except BadRequestKeyError:
            abort(403)


class Enterprise(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_enterprises'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.name = CharField(max_length=150)
        self.cnpj = IntField(display=CNPJ)
        self.phone = CharField(max_length=13, null=True, display=PHONE)
        self.active = BoolField(default_value=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.name = form['name']
            self.cnpj = load_int(['cnpj'])
            self.phone = load_int_as_str(['phone'])
            self.active = 'active' in form
        except BadRequestKeyError as ke:
            abort(403)


class MealCheck(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_meal_checks'
        self.create_connection = create_sige
        self.date = DateField(display=DATE)
        self.registry = IntField()
        self.has_meal = BoolField(default_value=False)
        self.bf_prepare()

    def load_from_web(self, txt, value):
        tmp = txt.split('_')
        tmp2 = tmp[3].split('.')
        this_date = load_date(tmp2[2], fmt='%d.%m.%Y')
        registry = int(tmp[2])
        qry = Query(self)
        qry.get(date=this_date, registry=registry, result_type=T_DICT)
        if len(qry) > 0:
            self.load_data(qry[0])
        try:
            self.date = this_date
            self.registry = registry
            self.has_meal = value == 'Y'
        except BadRequestKeyError as ke:
            abort(403)


class Report(BaseModel):
    choices = {'B': create_sige,
               'I': create_mss_inner,
               'M': create_mss_gate,
               'D': create_mss_driver,
               'E': create_mss_top,
               'W': create_oracle}

    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_reports'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.title = CharField(max_length=150)
        self.script = CharField(max_length=999999999)
        self.type = CharField(max_length=1, default_value='B',
                              choices=self.choices)
        self.recipients = CharField(max_length=1024, null=True)
        self.execution_start = TimeField(null=True, display=TIME)
        self.is_widget = BoolField(default_value=False)
        self.group = CharField(null=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.title = form['title']
            self.script = form['script'].split(';')[0]
            self.type = form['type']
            self.execution_start = load_time(form['execution_start'])
            self.is_widget = form['is_widget'] == 'Y'
            self.recipients = nwe(form['recipients'])
            self.group = nwe(form['group'])
        except BadRequestKeyError:
            abort(403)

    @property
    def parameters(self):
        qry = Query(ReportParameter)
        return qry.get(report=self.id)

    @property
    def rows_count(self):
        qry = Query(WidgetsData)
        qry.get(widget=self.id)
        if len(qry) > 0:
            return qry[0].rows_count

    @property
    def last_update(self):
        qry = Query(WidgetsData)
        qry.get(widget=self.id)
        if len(qry) > 0:
            return qry[0].last_update

    @property
    def report_connection(self):
        return self.choices[self.type]


class ReportParameter(BaseModel):
    choices = {'S': 'Text', 'N': 'Number', 'D': 'Date', 'T': 'Date and Hour'}

    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_report_parameters'
        self.create_connection = create_sige
        self.report = ForeignField(Report, field_name='rid')
        self.name = CharField(max_length=100)
        self.type = CharField(max_length=1, choices=self.choices,
                              default_value='S')
        self.default_value = CharField(null=True)
        self.legend = CharField(max_length=100, null=True)
        self.bf_prepare()

    def get_value(self):
        try:
            if self.type == 'S':
                return self.default_value
            elif self.type == 'N':
                return float(self.default_value)
            elif self.type == 'D':
                return datetime.strptime(self.default_value, '%d/%m/%Y').date()
            elif self.type == 'T':
                return datetime.strptime(self.default_value, '%d/%m/%Y %H:%M')
        except ValueError as ex:
            raise ValueError('{}\nThis value [{}] can\'t be '
                             'formated as {}'.format(ex, self.default_value,
                                                     self.choices[self.type]))


class Role(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_roles'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.name = CharField(max_length=100)
        self.active = BoolField(default_value=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.name = form['name']
            self.active = 'active' in form
        except BadRequestKeyError:
            abort(403)


class User(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_users'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.name = CharField()
        self.user = CharField()
        self.email = CharField(null=True)
        self.password = CharField(default_value=sha256(b'padrao').hexdigest())
        self.active = BoolField(default_value=True)
        self.xmpp_user = CharField(null=True)
        self.access = ForeignField(Access)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.name = form['name']
            self.user = form['user']
            self.email = nwe(form['email'])
            self.xmpp_user = nwe(form['xmpp_user'])
            self.active = 'active' in form
            if 'clear_password' in form:
                self.password = sha256(b'padrao').hexdigest()
        except BadRequestKeyError:
            abort(403)


class Vacancy(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_vacancys'
        self.create_connection = create_sige
        self.id = IntField(primary_key=True)
        self.relative_start = DateField(display=DATE)
        self.relative_end = DateField(display=DATE)
        self.use_start = DateField(display=DATE)
        self.use_end = DateField(display=DATE)
        self.allowance_start = DateField(null=True, display=DATE)
        self.allowance_end = DateField(null=True, display=DATE)
        self.employee = ForeignField(Employee, field_name='eid')
        self.observations = CharField(max_length=1024, null=True)
        self.document = BytesField(null=True)
        self.document_ext = CharField(max_length=5, null=True)
        self.bf_prepare()

    def load_from_web(self, form):
        try:
            self.relative_start = load_date(form['relative_start'])
            self.relative_end = load_date(form['relative_end'])
            self.use_start = load_date(form['use_start'])
            self.use_end = load_date(form['use_end'])
            self.allowance_start = load_date(form['allowance_start'])
            self.allowance_end = load_date(form['allowance_end'])
            self.observations = nwe(form['observations'])
            self.document_ext = replace_when_none(
                nwe(form['document_filename'].split('.')[-1]),
                self.document_ext)
            if len(form['document']) > 0:
                self.document = b64decode(
                    form['document'].split(';base64,')[1].encode())
        except BadRequestKeyError:
            abort(403)


class WidgetsData(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._bf_table_name = 'bf_widgets_data'
        self.create_connection = create_sige
        self.widget = ForeignField(Report, field_name='wid')
        self.last_update = DateTimeField(default_value=datetime(1900, 1, 1),
                                         display=DATETIME)
        self.rows_count = IntField(default_value=0)
        self.data = CharField(max_length=999999999)
        self.bf_prepare()

    def update_data(self, rid=None):
        report = Report()
        report.load(replace_when_none(rid, self.widget))
        connection = report.report_connection()
        rset = connection.query_with_columns(report.script)
        Query(self).get(widget=report.id).delete_all()
        if rset[1]:
            data = []
            for row in rset[1]:
                data.append(dict(zip(rset[0], all_as_str(row))))
            self.widget = report.id
            self.data = json.dumps(data)
            self.rows_count = len(data)
            self.last_update = datetime.now()
            self.save()
