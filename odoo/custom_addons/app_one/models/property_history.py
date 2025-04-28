from odoo import models, fields


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
    bedroom_ids = fields.One2many('property.history.bedroom', 'history_id')


class PropertyHistoryBedroom(models.Model):
    _name = 'property.history.bedroom'

    area = fields.Float()
    description = fields.Char()
    history_id = fields.Many2one('property.history')
