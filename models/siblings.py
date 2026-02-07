from odoo import fields, models, api


class Siblings(models.Model):
    _name = 'vm.siblings'
    _description = 'Description'

    student_id = fields.Many2one('vm.student', string='Student',required=True)
    name=fields.Char('Name',required=True)
    grade_id=fields.Many2one('vm.student.grade', string='Grade',required=True)
