from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError, AccessError, MissingError


class Stages(models.Model):
    _name = 'student.stages'
    _description = 'Student stages'

    _rec_name = 'name'
    _order = "sequence, name, id"



    sequence=fields.Integer(default=1)
    name = fields.Char(string="Stage Name")
    is_enrolled_student=fields.Boolean(default=False)
    mail_template_id=fields.Many2one('mail.template',string="Mail Template")
    state=fields.Selection([('new',"New"),("interview","Interview"),("student","Student"),("rejection","Rejection")],string="Status",default="interview")

    @api.constrains('is_enrolled_student')
    def check_is_student(self):
        if self.is_enrolled_student:
            stage_is_student= self.env['student.stages'].sudo().search([("is_enrolled_student","=",True),("id","!=",self.id)])
            if stage_is_student:
                raise ValidationError("Only One Stage Must be Enrolled For Students.")

    @api.constrains('state')
    def check_rejection(self):
        if self.state == 'rejection':
            stage_rejection = self.env['student.stages'].search([("id","!=",self.id),("state","=","rejection")])
            if stage_rejection:
                raise ValidationError("Only One Stage Must be Rejection For Students.")