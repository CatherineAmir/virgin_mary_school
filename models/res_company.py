from odoo import fields, models, api


class ModelName(models.Model):
    _inherit="res.company"
    vision=fields.Html(translate=True,string="Vision")
    mission=fields.Html(translate=True,string="Mission")