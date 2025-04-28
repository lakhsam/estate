from odoo import models, fields


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    property_ids = fields.One2many('property', 'owner_id', string='Property')