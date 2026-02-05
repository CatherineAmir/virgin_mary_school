from odoo import fields, models, api


class StudentGrades(models.Model):
    _name = 'vm.student.grade'
    _description = 'Student Grades'

    name = fields.Char(required=True,translate=True)
    open_for_admission = fields.Boolean(default=False)

