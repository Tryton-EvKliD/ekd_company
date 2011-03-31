# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of 
#this repository contains the full copyright notices and license terms. 
'Department'

'''
Департамент			 Department
Филиал				 Branch
Направления бизнеса		 Business Direction
Центр доходов			 Center Income
Центр затрат			 Center Costs
Отдел филиала предприятия	 Division branch office
Отдел предприятия		 Division of Enterprise

Административный отдел		 Administrative Division
Производственный отдел		 Production Department
Вспомогательный отдел		 Support Division
Информационный отдел		 Information Division
Отдел реализации		 Sales Department
Отдел снабжения			 Supply Division
Отдел перевозок			 Department of Transportation
Отдел доставки			 Delivery Division
Транспортный отдел		 Transport Department
Отдел обработки информации	 Department of Information Processing
Отдел сбора информации		 Department of gathering information
подотдел subdivision
Бухгалтерский отдел		Accounting Department
Складской отдел			Warehouse Division

Должность сотрудника		Officer position
Персонал			Staff
Кадровое			Staffing
Зарплата			Salary
Должность			Job function
Структура Предприятий

Головное предприятие (The parent company)
    Дочернее предприятие (Subsidiary company)
        Филиал предприятия (Branch Offices)
            Отдел филиала (Division branch office)
            Отдел филиала предприятия (Division branch office)
                Отдел предприятия (Division companies)
                    Отдел предприятия (Division companies)

        Филиал предприятия (Branch Offices)
            Отдел филиала (Division companies)

            Отдел предприятия (Division companies)

            Отдел предприятия (Division companies)
                Отдел предприятия (Division companies)



    Отдел предприятия (Division companies)

    Отдел предприятия (Division companies)
            Отдел предприятия (Division companies)

    Отдел предприятия (Division companies)
            Отдел предприятия (Division companies)
                Отдел предприятия (Division companies)

    Филиал предприятия (Branch Offices)
	Отдел компании (Division companies)

'''

from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction     
from trytond.pyson import Equal, Eval

_STATES = {
    'readonly': Equal(Eval('state'),'close'),
}

class Department(ModelSQL, ModelView):
    'Department'
    _name = 'ekd.company.department'
    _description = __doc__

    company = fields.Many2One('company.company', 'Company',
                ondelete="RESTRICT")
    name = fields.Char('Name', required=True, translate=True)
    shortname = fields.Char('ShortName', required=True, translate=True)
    parent = fields.Many2One('ekd.company.department', 'Parent',
                ondelete="RESTRICT")
    childs = fields.One2Many('ekd.company.department', 'parent', 'Subdivision')
    chief = fields.Many2One('company.employee', 'Chief of Division')
    employees = fields.One2Many('company.employee', 'department', 'Employees of department',
                                context={
                                    'company': Eval('company'), 
                                    'department':Eval('department')})
    start_date = fields.Date('Date Start')
    end_date = fields.Date('Date End')
    code = fields.Char('Code', required=True)
    note = fields.Text('Note')
    state = fields.Selection([
            ('planned', 'Planned'),
            ('active', 'Active'),
            ('closed', 'Closed'),
            ], 'State', readonly=True, required=True)
    type_department = fields.Selection([
            ('purchase', 'Purchase'),
            ('sales', 'Sales'),
            ('delivery', 'Delivery'),
            ('workshop', 'Workshop'),
            ('account', 'Account'),
            ('admin', 'Administrative Division'),
            ('warehouse', 'Warehouse'),
            ('shop', 'Shop'),
            ('other', 'Other'),
            ], 'Type', required=True, states=_STATES, select=1)
    active = fields.Boolean('Active')
    as_stock = fields.Boolean('As Stock')

    def default_company(self):
        return Transaction().context.get('company') or False

    def default_state(self):
        return 'planned'

    def default_active(self):
        return True

    def default_type_department(self):
        return 'other'

    def create(self, vals):
        new_id = super(Department, self).create(vals)
        if vals.get('as_stock'):
            cursor = Transaction().cursor
            cursor.execute('INSERT INTO ekd_company_department_stock'\
                    ' (id, create_uid, department)'\
                    'VALUES (%s, %s, %s)',\
                    (new_id, Transaction().user, new_id))
            cursor.commit()
        return new_id

    def write(self, ids, vals):
        cursor = Transaction().cursor
        if vals.get('as_stock'):
            for id_ in ids:
                cursor.execute('INSERT INTO ekd_company_department_stock'\
                    ' (id, create_uid, department)'\
                    'VALUES (%s, %s, %s)',\
                    (id_, Transaction().user, id_))
            cursor.commit()
        else:
            cursor.execute('DELETE FROM ekd_company_department_stock'\
                    ' WHERE id = %s'%(ids))
            cursor.commit()

        return super(Department, self).write(ids, vals)

Department()

class DepartmentStock(ModelSQL, ModelView):
    'Department'
    _name = 'ekd.company.department.stock'
    _description = __doc__
    _inherits = {'ekd.company.department': 'department'}

    department = fields.Many2One('ekd.company.department', 'Department',
            required=True, ondelete='CASCADE', select=1)

DepartmentStock()