import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    ref = fields.Char(default='New', required=True)
    description = fields.Text()
    postcode = fields.Char(required=True, size=5)
    date_availability = fields.Date(default=fields.Date.today, track_visibility=True)
    expected_selling_date = fields.Date(default=fields.Date.today, track_visibility=True)
    created_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute= '_compute_next_time')
    is_late = fields.Boolean()
    active = fields.Boolean(default=True)
    expected_price = fields.Float()
    selling_price = fields.Float(digits=(0,3))
    diff = fields.Float(compute='_compute_diff', store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          default='north'
    )

    owner_id = fields.Many2one('owner', string='Owner')
    tag_ids = fields.Many2many('tag', string='Tags')

    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', store=True)

    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('sold','Sold'), ('closed','Closed')], default='draft', tracking=True)

    bedroom_ids = fields.One2many('property.bedroom', 'property_id')

    # database check unicity
    _sql_constraints = [(
        'unique_name', 'unique(name)', 'Name must be unique!'
    )]

    def action_env(self):
        print(self.env['owner'].create({
            'name': self.env.user.name,
            'phone': self.env.company.phone,
        }))

    def action(self):
        print(self.env['property'].search(['|', ('name', '=', '33333')]))

    @api.depends('created_time')
    def _compute_next_time(self):
        for record in self:
            if record.created_time:
                record.next_time = record.created_time + datetime.timedelta(hours=6)
            else:
                record.next_time = False

    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for record in self:
            record.diff = record.expected_price - record.selling_price


    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for record in self:
            print("_onchange_expected_price")
            return {
                'warning': {'title': 'warning', 'message': 'negative value', 'type': 'notification'}
            }

    # logic layer check
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Bedrooms must be greater than 0.')


    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True



    def action_open_change_state(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_property_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    # CRUD Operations
    # Create
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_sequence')
        # Override logic
        print("Override create")
        return res

    # Read
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset, limit, order, access_rights_uid)
        print("Override _search")
        return res

    # Read
    def write(self, vals):
        res = super(Property, self).write(vals)
        print("Override write")
        return res

    # UnLink
    def unlink(self):
        res = super(Property, self).unlink()
        print("Override unlink")
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'property_id': rec.id,
                'user_id': self.env.uid,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'bedroom_ids': [(0, 0, {'area': line.area, 'description': line.description}) for line in rec.bedroom_ids],
            })


class PropertyBedroom(models.Model):
    _name = 'property.bedroom'

    property_id = fields.Many2one('property', string='Property')
    area = fields.Float()
    description = fields.Char()
