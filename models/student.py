from odoo import fields, models, api


class VmStudent(models.Model):
    _name = 'vm.student'
    _description = 'Full Student Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}


    name = fields.Char()
    name_arabic = fields.Char()
    birth_date = fields.Date('Birth Date')
    age_on_october = fields.Date('Age on October 2026')
    place_of_birth = fields.Char(string="Place of Birth")
    id_number = fields.Char("Student National ID")
    nationality = fields.Many2one('res.country', 'Nationality')

    number_of_brothers = fields.Integer('Number of Brothers')
    number_of_sisters=fields.Integer('Number of Sisters')

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

    grade_id=fields.Many2one('vm.student.grade', 'Grade',required=True, ondelete="restrict")
    parent_marital_status = fields.Selection([
        ("married","Married"),
        ("separated","Separated"),
        ("married","Married"),
        ("divorced","Divorced"),
        ("widow(er)","Widow(er)"),
    ])

    parent_ids = fields.Many2many('vm.parent', string='Parent')

    @api.model_create_multi
    def create(self, vals):
        res = super(VmStudent, self).create(vals)
        for values in vals:
            if values.get('parent_ids', False):
                for parent_id in res.parent_ids:
                    if parent_id.user_id:
                        user_ids = [student.user_id.id for student
                                    in parent_id.student_ids if student.user_id]
                        parent_id.user_id.child_ids = [(6, 0, user_ids)]
        return res

    def write(self, vals):
        res = super(VmStudent, self).write(vals)
        if vals.get('parent_ids', False):
            user_ids = []
            if self.parent_ids:
                for parent in self.parent_ids:
                    if parent.user_id:
                        user_ids = [parent.user_id.id for parent in parent.student_ids
                                    if parent.user_id]
                        parent.user_id.child_ids = [(6, 0, user_ids)]
            else:
                user_ids = self.env['res.users'].search([
                    ('child_ids', 'in', self.user_id.id)])
                for user_id in user_ids:
                    child_ids = user_id.child_ids.ids
                    child_ids.remove(self.user_id.id)
                    user_id.child_ids = [(6, 0, child_ids)]
        if vals.get('user_id', False):
            for parent_id in self.parent_ids:
                child_ids = parent_id.user_id.child_ids.ids
                child_ids.append(vals['user_id'])
                parent_id.name.user_id.child_ids = [(6, 0, child_ids)]
        self.env.registry.clear_cache()
        return res

    def unlink(self):
        for record in self:
            if record.parent_ids:
                for parent_id in record.parent_ids:
                    child_ids = parent_id.user_id.child_ids.ids
                    child_ids.remove(record.user_id.id)
                    parent_id.name.user_id.child_ids = [(6, 0, child_ids)]
        return super(VmStudent, self).unlink()

    def get_parent(self):
        self.ensure_one()
        action = self.env.ref(
            'virgin_mary_school.act_open_op_parent_view').sudo().read()[0]
        action['domain'] = [('student_ids', 'in', self.ids)]
        action['context'] = {'default_student_ids': [(6, 0, self.ids)]}
        return action
