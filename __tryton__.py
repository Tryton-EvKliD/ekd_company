# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Company',
    'name_de_DE': 'Unternehmen',
    'name_es_CO': 'Compañía',
    'name_es_ES': 'Empresa',
    'name_fr_FR': 'Société',
    'name_ru_RU': 'Учетные организации',
    'version': '1.8.0',
    'author': 'Dmitry Klimanov',
    'email': 'info@b2ck.com',
    'website': 'http://www.tryton.org/',
    'description': '''Define company and employee.
    Add main and current company on users preferences.
    Add company on properties.
    Define new report parser for report with company header.
    Add letter template on party.
    Make the scheduler run on each companies.
    ''',
    'description_ru_RU': '''Учет организаций и сотрудников.
    - Добавление основной и дочерних организаций
    - Добавление учетных организаций и свойств
    - Настройка отчетов для печати на фирменных бланках.
    - Добавление шаблона письма.
    - Устанавливает планировщика на работу с каждой учетной организацией.
    ''',
    'description_de_DE': ''' - Ermöglicht die Eingabe von Umternehmen und Mitarbeitern.
 - Fügt Haupt- und aktuelles Unternehmen zu den Benutzereinstellungen hinzu.
 - Fügt das Unternehmen den Eigenschaften hinzu.
 - Ermöglicht die Definition eines neuen Berichtsanalysierers mit Unternehmen im Berichtskopf.
 - Fügt den Kontakten die Berichtsvorlage für Briefe hinzu.
 - Initialisiert die Aufgaben des Zeitplaners für jedes Unternehmen.
''',
    'description_es_CO': ''' - Define compañía y empleados.
 - Añade compañía principal y predeterminada de acuerdo a preferencia de usuarios.
 - Añade compañía a las propiedades.
 - Define un nuevo reporteador para los encabezados de los reportes por compañía.
 - Añade plantilla de carta a un tercero.
 - Se ejecuta el agendador por compañía.
''',
    'description_es_ES': '''Define empresa y empleados.
 - Añade la empresa principal y predeterminada en las preferencias de los usuarios.
 - Añade empresa a las propiedades.
 - Define un nuevo analizador de informe para los informes con el encabezado de la empresa.
 - Añade una plantilla de carta en terceros.
 - Hace que el programador de tareas se ejecute por empresa.
''',
    'description_fr_FR': '''Défini société et employé.
Ajoute les sociétés principale et courante dans les préférences de l'utilisateur.
Ajoute la société sur les propriétés.
Défini un nouveau moteur de rapport gérant une entête par société.
Ajoute un canva de lettre par tiers.
Lance les planificateurs sur chaque société.
''',
    'depends': [
        'ir',
        'res',
        'party',
        'currency',
        'company',
        'ekd_system',
        'ekd_party',
    ],
    'xml': [
        'xml/company.xml',
        'xml/employee.xml',
        'xml/employee_promo.xml',
        'xml/employee_research.xml',
        'xml/ekd_party.xml',
        'xml/ekd_system.xml',
        'xml/jobfunction.xml',
        'xml/ekd_department.xml',
        'xml/ekd_staff_list.xml',
        'xml/ekd_stock.xml',
    ],
    'translation': [
        'ru_RU.csv',
    ]
}
