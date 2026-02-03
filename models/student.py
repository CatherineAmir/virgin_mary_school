from odoo import fields, models, api


class student(models.Model):
    _name = 'vm.student'
    _description = 'Full Student Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin',"utm.mixin"]
    _inherits = {"res.partner": "partner_id"}


    name = fields.Char()
    name_arabic = fields.Char()
    birth_date = fields.Date('Birth Date')
    age_on_october = fields.Date('Age on October 2026')
    place_of_birth = fields.Char(string="Place of Birth")
    id_number = fields.Char("Student National ID")
    nationality = fields.Many2one('res.country', 'Nationality')

    def _compute_stage_id(self):
        for student in self:
            if not student.stage_id:
                stage = self.env['student.stages'].search([], order="sequence,id", limit=1)
                if stage:
                    return stage.id



    stage_id = fields.Many2one('student.stages', string='Student Stage', default=_compute_stage_id, store=True,
                               index=True, tracking=True, copy=False, ondelete='restrict', )



    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),

    ], 'Gender', required=True, default='m')

    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('christian', 'Christian'),

    ], 'Gender', required=True, default='christian')

    detailed_address = fields.Char('Detailed Address in Arabic')

    transportation = fields.Selection([('Bus', "bus"), ("Other", "other")], string='Transportation')

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    active = fields.Boolean(default=True)

    # Related to the stage record
    is_enrolled_student = fields.Boolean(related="stage_id.is_enrolled_student", store=True)

