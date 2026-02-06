from odoo import fields, models, api


class StudentGrades(models.Model):
    _name = 'vm.student.grade'
    _description = 'Student Grades'

    name = fields.Char(required=True,translate=True)
    open_for_admission = fields.Boolean(default=False)
    parent_id=fields.Many2one('vm.student.grade',string="Parent Grade",domain="[('id','!=',id),('is_parent','=',True)]")
    is_parent=fields.Boolean(default=False)
    sequence = fields.Integer()

