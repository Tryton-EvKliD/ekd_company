# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from __future__ import with_statement
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard
from trytond.report import Report
from trytond.pyson import Equal, Eval, Get, PYSONEncoder
from trytond.transaction import Transaction
from decimal import Decimal
import datetime

class Staff(ModelSQL, ModelView):
    'Staff'
    _name = 'ekd.company.staff'
    _description = __doc__

    company = fields.Many2One('company.company', 'Company', required=True)
    name = fields.Char('Name', size=None, required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    line = fields.One2Many('ekd.company.staff.list', 'staff', 'Lines')
    active = fields.Boolean('Active')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archive', 'Archive'),
        ], 'State', readonly=True, required=True, select=1)

    def default_company(self):
        return  Transaction().context.get('company') or False

Staff()

class StaffList(ModelSQL, ModelView):
    'Staff list'
    _name = 'ekd.company.staff_list'
    _description = __doc__

    company = fields.Many2One('company.company', 'Company', required=True)
    staff = fields.Many2One('ekd.company.staff', 'Staff list')
    department = fields.Many2One('ekd.company.department', 'Department')
    name = fields.Char('Name', size=None, required=True)
    job_function = fields.Many2One('ekd.company.job_function', 'Job function')
    category = fields.Many2One('ekd.company.employee.category', 'Category')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    regular = fields.Boolean('Regular appointment')
    free_rate = fields.Function(fields.Float('Free of bets', digits=(3,3)), 'get_free_rate')
    #schedule = fields.Many2One('ekd.timesheet.schedule', 'Schedule')
    payroll = fields.Selection([
        ('hourly','Hourly rates'),
        ('dayly','Daily rate'),
        ('monthly','Monthly salary')
        ], 'Accounting payroll')
    rate_payroll = fields.Function(fields.Numeric('Rate payroll', digits=(16,2)), 'get_rate_payroll')
    time_management = fields.Selection([('in_day','In Day'),('in_hour','In Hour')], 'Time management')
    work_rate = fields.Float('Number of bets', digits=(3,3))
    personal = fields.One2Many('ekd.company.employee.account', 'staff_list', 'Employee')
    payroll = fields.One2Many('ekd.company.staff_list.payroll', 'staff_list', 'Payroll')
    active = fields.Boolean('Active')
    note = fields.Text('Note')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archive', 'Archive'),
        ], 'State', readonly=True, required=True, select=1)

    #def __init__(self):
    #    super(StaffList, self).__init__()

    def default_company(self):
        return  Transaction().context.get('company') or False

    def get_free_rate(self, ids, name):
        res={}.fromkeys(ids, 0.0)
        for line in self.browse(ids):
            res[line.id] = line.work_rate
            for employee in line.personal:
                res[line.id] -= employee.work_rate

    def get_rate_payroll(self, ids, name):
        res={}.fromkeys(ids, Decimal('0.0'))
        for line in self.browse(ids):
            for rate_payroll in line.payroll:
                res[line.id] += rate_payroll.rate

StaffList()

class StaffListPayroll(ModelSQL, ModelView):
    'Staff list Payroll'
    _name = 'ekd.company.staff_list.payroll'
    _description = __doc__

    staff_list = fields.Many2One('ekd.company.staff_list', 'Staff list')
    name = fields.Char('Name', size=None, required=True)
    sequence = fields.Integer('Sequence')
    rate = fields.Numeric('Rate', digits=(16, Eval('currency_digits', 2)))
    coefficient = fields.Numeric('Coefficient', digits=(3, 2))
    type_coefficient = fields.Selection([('percent','Percect'),('rate','Rate')], 'Type Coefficient')
    currency = fields.Many2One('currency.currency', 'Currency')
    currency_digits = fields.Function(fields.Integer('Currency Digits'), 'get_currency_digits')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    def get_currency_digits(self, ids, names):
        res = {}.fromkeys(ids, 2)
        for line in self.browse(ids):
            if line.currency:
                res[line.id] = line.currency.digits
            else:
                res[line.id] = line.staff_list.company.currency.digits
        return res

StaffListPayroll()

class PersonalAccount(ModelSQL, ModelView):
    'Personal account'
    _name = 'ekd.company.employee.account'
    _description = __doc__

    staff_list = fields.Many2One('ekd.company.staff_list', 'Staff list')
    employee = fields.Many2One('company.employee', 'Employee')
    work_rate = fields.Float('Number of bets', digits=(3,3))
    active = fields.Boolean('Active')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archive', 'Archive'),
        ], 'State', readonly=True, required=True, select=1)

PersonalAccount()
