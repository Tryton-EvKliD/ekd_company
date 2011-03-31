# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
"Company"
from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction
import copy
import datetime

class CompanyJobFunction(ModelSQL, ModelView):
    'Company Job Function'
    _name = 'ekd.company.job_function'
    _description = __doc__

    company = fields.Many2One('company.company', 'Company', required=True)
    name = fields.Char('Name', size=None, required=True)
    shortname = fields.Char('Short Name', size=32, required=True)
    note = fields.Text('Note')
    pay_period = fields.Selection([
                        ('daily','Daily'),
                        ('weekly','Weekly'),
                        ('monthly','Monthly'),
                        ('other','Other')
                        ],'Salary Period')
    type_timesheet = fields.Selection([
                        ('daily','Daily'),
                        ('hourly','Hourly'),
                        ('piece_rate','Piece-rate'),
                        ('other','Other')
                        ],'Type Timesheet')
    salary = fields.Numeric('Salary', digits=(16,2))
    premium = fields.Numeric('Premium', digits=(16,2))

    def default_company(self):
        return Transaction().context.get('company') or False

    def get_rec_name(self, ids, name):
        if not ids:
            return []
        res = {}
        for jobs in self.browse(ids):
            if jobs.shortname:
                res[jobs.id] = jobs.shortname
            else:
                res[jobs.id] = jobs.name
        return res

CompanyJobFunction()
