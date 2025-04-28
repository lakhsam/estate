from odoo import models, fields


class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'code'

    no = fields.Integer(string='No')
    code = fields.Char(string='Code')
    description = fields.Char(string='description')
    active = fields.Boolean(default=True)