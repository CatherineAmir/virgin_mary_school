from odoo import fields, models, api


class StudentPortal(models.Model):
    _inherit = 'res.partner'

    is_parent = fields.Boolean("Is a Parent")
    is_student = fields.Boolean("Is a Student")
    _unique_email = models.Constraint('unique(email)',
                                      'Email must be unique per partner!')
