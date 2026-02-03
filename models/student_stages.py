from odoo import fields, models, api


class Stages(models.Model):
    _name = 'student.stages'
    _description = 'Student stages'

    _rec_name = 'name'
    _order = "sequence, name, id"



    sequence=fields.Integer(default=1)
    name = fields.Char(string="Stage Name")
    is_enrolled_student=fields.Boolean(default=False)
    mail_template_id=fields.Many2one('mail.template',string="Mail Template")
