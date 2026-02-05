
from odoo import fields, models


class vmParentRelation(models.Model):
    _name = "vm.parent.relationship"
    _description = "Relationships"

    name = fields.Char('Name', required=True)

    _unique_relationship_name = models.Constraint(
        'unique(name)', 'Can not create relationship multiple times.!')
