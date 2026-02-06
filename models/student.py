from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class VmStudent(models.Model):
    _name = 'vm.student'
    _description = 'Full Student Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}


    # name = fields.Char()

    name_arabic = fields.Char()
    birth_date = fields.Date('Birth Date')
    age_on_october = fields.Char('Age on October',compute='_compute_age_on_october')
    place_of_birth = fields.Char(string="Place of Birth")
    national_id = fields.Char("Student National ID")
    nationality = fields.Many2one('res.country', 'Nationality')

    number_of_brothers = fields.Integer('Number of Brothers')
    number_of_sisters=fields.Integer('Number of Sisters')
    current_academic_year=fields.Many2one('vm.academic.year', 'Current Academic Year')
    date_required=fields.Date('Required for Application',related='current_academic_year.date_required_for_application')
    age_year=fields.Integer('Age Year',compute='_compute_age_on_october',store=True,compute_sudo=True)
    age_month=fields.Integer('Age Month',compute='_compute_age_on_october',store=True,compute_sudo=True)
    age_day=fields.Integer('Age day',compute='_compute_age_on_october',store=True,compute_sudo=True)


    @api.depends('birth_date',"date_required")
    def _compute_age_on_october(self):
        for r in self:
            if r.date_required and r.birth_date:
                diff=relativedelta(r.date_required,r.birth_date)
                r.age_year = diff.years
                r.age_month = diff.months
                r.age_day = diff.days
                r.age_on_october = f"{diff.years} years, {diff.months} months, {diff.days} days"
            else:
                r.age_on_october = ""

    def _compute_stage_id(self):
        stage = self.env['student.stages'].search([], order="sequence,id", limit=1)
        if stage:
            return stage.id



    stage_id = fields.Many2one('student.stages', string='Student Stage', default=_compute_stage_id,
                               index=True, tracking=True, copy=False, ondelete='restrict', )



    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),

    ], 'Gender', required=True, default='male')

    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('christian', 'Christian'),

    ], 'Religion', required=True, default='christian')

    detailed_address = fields.Char('Detailed Address in Arabic')

    transportation = fields.Selection([('bus', "Bus"), ("other", "Other")], string='Transportation')

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade", delegate=True)
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
    legal_custodian=fields.Selection([("father","Father"),("mother","Mother"),("other","Other")],string="Legal Custodian",default='father')


    parent_ids = fields.Many2many('vm.parent', string='Parent')
    previous_school_name=fields.Char('Previous School Name')

    _unique_national_id = models.Constraint('unique(national_id)',
                                      'National Id must be unique per student!')

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
