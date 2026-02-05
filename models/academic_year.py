from odoo import fields, models, api


class AcademicYear(models.Model):
    _name = 'vm.academic.year'
    _description = "Academic Year"

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    current_year=fields.Boolean('Current Year')
    admission_open=fields.Boolean('Admission Open')

    medical_survey_id=fields.Many2one('survey.survey', 'Medical Survey Template')

    required_documents = fields.Html('Required Docs')
    parent_contact_confirmation = fields.Html('Parent Contact Confirmation')


