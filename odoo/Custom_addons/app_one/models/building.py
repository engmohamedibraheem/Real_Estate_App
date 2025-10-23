from odoo import models,fields

class Building(models.Model):
    #Table by ORM
    _name='building'
    _description = 'Building'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'code'

    #Fields
    no = fields.Integer()
    code=fields.Char()
    description=fields.Text()
    #Reserved fields
    name=fields.Char()
    active=fields.Boolean(default=True)