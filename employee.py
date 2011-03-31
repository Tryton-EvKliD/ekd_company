# -*- coding: utf-8 -*-
"Company"
import copy
from trytond.model import ModelStorage, ModelView, ModelSQL, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval, Not, Bool
from trytond.wizard import Wizard
from trytond.report import Report
from trytond.modules.ekd_party.images import female, male
import datetime

STATES = {
        'readonly': Not(Bool(Eval('active'))),
    }
SEPARATOR = ' / '

class CategoryEmployee(ModelSQL, ModelView):
    "Category"
    _name = "ekd.company.employee.category"
    _description = __doc__
    name = fields.Char('Name', required=True, states=STATES)
    shortname = fields.Char('ShortName', required=True, states=STATES)
    parent = fields.Many2One('ekd.company.employee.category', 'Parent',
           select=1, states=STATES)
    childs = fields.One2Many('ekd.company.employee.category', 'parent',
       'Children', states=STATES)
    active = fields.Boolean('Active')

    def __init__(self):
        super(CategoryEmployee, self).__init__()
        self._sql_constraints = [
            ('name_parent_uniq', 'UNIQUE(name, parent)',
                'The name of a party category must be unique by parent!'),
        ]
        self._constraints += [
            ('check_recursion', 'recursive_categories'),
            ('check_name', 'wrong_name'),
        ]
        self._error_messages.update({
            'recursive_categories': 'You can not create recursive categories!',
            'wrong_name': 'You can not use "%s" in name field!' % SEPARATOR,
        })
        self._order.insert(1, ('name', 'ASC'))

    def default_active(self):
        return 1

    def check_name(self, ids):
        for category in self.browse(ids):
            if SEPARATOR in category.name:
                return False
        return True

    def get_rec_name(self, ids, name):
        if not ids:
            return {}
        res = {}
        def _name(category):
            if category.id in res:
                return res[category.id]
            elif category.parent:
                return _name(category.parent) + SEPARATOR + category.name
            else:
                return category.name
        for category in self.browse(ids):
            res[category.id] = _name(category)
        return res

    def search_rec_name(self, name, clause):
        if isinstance(clause[2], basestring):
            values = clause[2].split(SEPARATOR)
            values.reverse()
            domain = []
            field = 'name'
            for name in values:
                domain.append((field, clause[1], name))
                field = 'parent.' + field
            ids = self.search(domain, order=[])
            return [('id', 'in', ids)]
        #TODO Handle list
        return [('name',) + clause[1:]]

CategoryEmployee()

class Employee(ModelSQL, ModelView):
    'Employee'
    _name = 'company.employee'
    _description = __doc__
    _inherits = {'party.party': 'party'}
#    _rec_name = 'shortname'

    party = fields.Many2One('party.party', 'Person', required=True)
    department = fields.Many2One('ekd.company.department', 'Department')
    job_function = fields.Many2One('ekd.company.job_function', 'Officer position')
    company = fields.Many2One('company.company', 'Company', required=True)
    uid_employee = fields.Char('UID Officer', size=10)
    pension_number = fields.Char('Pension Number', size=20)
    social_number = fields.Char('Social Number', size=20)
    peripatetic = fields.Boolean('Peripatetic')
    gender = fields.Selection([('male','Male'),('female','Female')], 'Gender')
    marital = fields.Selection([
                    ('maried','Maried'),
                    ('unmaried','Unmaried'),
                    ('divorced','Divorced'),
                    ('civil_marriage','Civil Marriage'),
                    ('other','Other')
                    ],'Marital Status')
    starting_date = fields.Date('Starting Date')
    dismissal_date = fields.Date('Date dismissal')
    medical_date = fields.Date('Date of medical review')
    fluro_date = fields.Date('Date Flyurografiya')
    education = fields.Selection([
                    ('primary','Primary Edu'),
                    ('secondary','Secondary Edu'),
                    ('special','Special Edu'),
                    ('higher','Higher Edu')
                    ], 'Education')
    prof_education = fields.Char('Profession Education')
    properties = fields.One2Many('company.employee.properties', 'employee', 'Advanced Properties')
    children = fields.One2Many('company.employee.children', 'employee', 'Children of Employee')
    educations = fields.One2Many('company.employee.education', 'employee', 'Educations')
    experience = fields.One2Many('company.employee.experience', 'employee', 'Work Experience')
    personal_account = fields.One2Many('ekd.company.employee.account', 'employee', 'Personal Accounts')
#    calendar = fields.Many2One('calendar.calendar', 'Calendar')
    state = fields.Selection([
                    ('work','At work'),
                    ('in_trip','In trip'),
                    ('sick','Sick'),
                    ('on_leave','On leave'),
                    ('on_parental_leave','On parental leave'),
                    ('pending','Pending'),
                    ('reserve','Reserve'),
                    ('at_project','At project'),
                    ('dismissed','Dismissed'),
                    ], 'State')
#    area_residence = fields.Many2One('country.subdivision','Area of residence')

    def default_individual(self):
        return True

    def default_employee(self):
        return True

    def default_photo(self):
        return female

    def default_company(self):
        return Transaction().context.get('company') or False

    def default_department(self):
        return Transaction().context.get('department') or False

    def get_rec_name(self, ids, name):
        if not ids:
            return []
        res = {}
        for party in self.browse(ids):
            if party.shortname:
                res[party.id] = party.shortname
            else:
                res[party.id] = party.name
        return res

    def create(self, vals):
        cursor = Transaction().cursor
        if vals.get('from_party', False):
            cursor.execute('INSERT INTO ' +self._table +\
                    ' (id, create_uid, party, company, peripatetic)'\
                    'VALUES (%s, %s, %s, %s, %s)',\
                    (vals.get('id'), vals.get('create_uid'), vals.get('party'), Transaction().context.get('company'), False))
            cursor.commit()
            res = self.browse(vals.get('id'))
            return res.id
        else:
            later = {}
            vals = vals.copy()
            for field in vals:
                if field in self._columns\
                    and hasattr(self._columns[field], 'set'):
                        later[field] = vals[field]
            for field in later:
                del vals[field]
            if cursor.nextid(self._table):
                cursor.setnextid(self._table, cursor.currid(self._table))
            new_id = super(Employee, self).create(vals)
            employee = self.browse(new_id)
            new_id = employee.party.id
            cursor.execute('UPDATE "' + self._table + '" SET id = %s '\
                            'WHERE id = %s', (employee.party.id, employee.id))
            ModelStorage.delete(self, employee.id)
            self.write(new_id, later)
            res = self.browse(new_id)
            return res.id

Employee()

class CompanyEmployeeProperties(ModelSQL, ModelView):
    'Properties'
    _description=__doc__
    _name = 'company.employee.properties'

    employee = fields.Many2One('company.employee', 'Employee', ondelete='CASCADE', required=True)
    key = fields.Char('Type value')
    value = fields.Char('Value')
    active = fields.Boolean('Active')

CompanyEmployeeProperties()

class CompanyEmployeeEducation(ModelSQL, ModelView):
    'Education'
    _description=__doc__
    _name = 'company.employee.education'

    employee = fields.Many2One('company.employee', 'Employee', ondelete='CASCADE', required=True)
    date_start = fields.Date('Start date')
    date_end = fields.Date('End date')
    name = fields.Char('Education Name')
    prof_education = fields.Char('Profession Education')

CompanyEmployeeEducation()

class CompanyEmployeeChildren(ModelSQL, ModelView):
    'Children of Employees'
    _description=__doc__
    _name = 'company.employee.children'

    employee = fields.Many2One('company.employee', 'Employee', ondelete='CASCADE', required=True)
    name = fields.Char('Full Name')
    birthday = fields.Date('Birthday')
    gender = fields.Selection([
                ('male','Male'),
                ('female','Female')
                ], 'Gender')
    place = fields.Char('Place of Study')

CompanyEmployeeChildren()

class CompanyEmployeeExperience(ModelSQL, ModelView):
    'Work Experience'
    _description=__doc__
    _name = 'company.employee.experience'

    employee = fields.Many2One('company.employee', 'Employee', ondelete='CASCADE', required=True)
    date_start = fields.Date('Start date')
    date_end = fields.Date('End date')
    company = fields.Char('Company')
    function = fields.Char('Function')

CompanyEmployeeExperience()
