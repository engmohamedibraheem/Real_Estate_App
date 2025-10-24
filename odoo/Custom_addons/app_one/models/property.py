from email.policy import default

from dateutil.utils import today

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class Property(models.Model):
    # Table by ORM
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Create Fields as a Colum
    ref=fields.Char(default="New",readonly=1)
    name = fields.Char(required=1, default='Bakous! etc.', size=20, tracking=1)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=today())
    expected_selling_date = fields.Date()
    is_late=fields.Boolean()
    expected_price = fields.Float(required=1, digits=(5, 2))
    selling_price = fields.Float()
    diff = fields.Float(compute='_onchange_expected_price', store=1)  # readonly=0
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          default='north')
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('sold', 'Sold'), ('closed', 'Closed')],
                             default='draft')
    active = fields.Boolean(default=True)
    # Relatoonal Fields
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    lines_ids = fields.One2many('property.line', 'property_id')
    # Related Field ==> we can use both related attribute and computed attribute
    owner_phone = fields.Char(related='owner_id.phone')  # readonly=0 ,store=1 ==> we can use computed fields
    owner_address = fields.Char(related='owner_id.address')  # readonly=0 ,store=1

    # Data base Tier validation
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    # Compute Method
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("inside compute difference")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price', 'selling_price', 'owner_id.phone')
    def _onchange_expected_price(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price
        print("inside _onchange_expected_price method")

    # logic Validation
    @api.constrains('expected_price')
    def _check_expected_price_equal_zero(self):
        for rec in self:
            if rec.expected_price == 0:
                raise ValidationError('please add valid number of expected price')

    # CURD Operation Methods
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref=self.env['ir.sequence'].next_by_code('property_Seq')
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside the search method")
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        print("Inside write method")
        return res

    def unlink(self):
        res = super(Property, self).unlink()
        print("Inside unlike method")
        return res

    # Status bar function
    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state = 'draft'
            # rec.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state,'pending')
            rec.write({
                'state': 'pending'
            })

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state,'sold')
            rec.state = 'sold'

    def action_close(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    #cron job
    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date <fields.date.today():
                rec.is_late=True

    def create_history_record(self,old_state,new_state,reason=" "):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id':rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason,
            })
    def change_open_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context']={'default_property_id':self.id}
        return action

# Model To be Notebook
class PropertyLine(models.Model):
    _name = 'property.line'

    Area = fields.Float()
    Description = fields.Char()
    property_id = fields.Many2one('property')
