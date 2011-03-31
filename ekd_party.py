# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelStorage, ModelView, ModelSQL, fields
from trytond.transaction import Transaction

class Party(ModelSQL, ModelView):
    _name = "party.party"

    employee = fields.Boolean('Employee', readonly=True, select=2, help="Check this box if the party is a Employee.")
    manager = fields.Many2One('company.employee', 'Responsible Officer',)

    def create(self, vals):
        new_id = super(Party, self).create(vals)
        if vals.get('employee', False):
            employee_obj = self.pool.get('company.employee')
            employee_obj.create({
                                'from_party': True,
                                'create_uid': Transaction().user,
                                'company': Transaction().context.get('company', False),
                                'party': new_id,
                                })
        return new_id

    def write(self, ids, vals):
        if vals.get('employee'):
            employee_obj = self.pool.get('company.employee')
            if not employee_obj.search([('party','=', ids[0])]):
                employee_obj.create({
                                'party': ids[0],
                                })
        else:
            if vals.get('employee', True):
                pass
            else:
                employee_obj = self.pool.get('company.employee')
                if employee_obj.search([('party','=', ids[0])]):
                    employee_obj.delete(ids)

        return super(Party, self).write(ids, vals)

Party()
