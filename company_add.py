#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
"Company"
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval
import copy


class Company(ModelSQL, ModelView):
    _name = 'company.company'

    employees = fields.One2Many('company.employee', 'company', 'Employees')
    ceo = fields.Many2One('company.employee', 'Chief Executive Officer')
    cfo = fields.Many2One('company.employee', 'Chief Finance Officer')
    ceo2 = fields.Many2One('company.employee', 'Chief Economic Officer')
    cao = fields.Many2One('company.employee', 'Chief Accountant')
    cco = fields.Many2One('company.employee', 'Chief Cashier')
    cpo = fields.Many2One('company.employee', 'Chief Personnel Officer')

Company()

class User(ModelSQL, ModelView):
    _name = 'res.user'

    employee = fields.Many2One('company.employee', 'Employee',
                domain=[('company', 'child_of', [Eval("main_company")], 'parent')])

User()

class Employee(ModelSQL, ModelView):
    _name = 'company.employee'

    job_function = fields.Many2One('ekd.company.job_function', 'Officer position')

Employee()