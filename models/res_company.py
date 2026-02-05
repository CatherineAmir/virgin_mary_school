from odoo import fields, models, api


class ModelName(models.Model):
    _inherit="res.company"
    vision=fields.Html(transalte=True,string="Vision")
    mission=fields.Html(transalte=True,string="Mission")