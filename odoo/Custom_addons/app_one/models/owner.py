from odoo import models,fields,api

class Owner(models.Model):
    #Table by ORM
    _name='owner'

    name = fields.Char(required=1, default='Mostafa etc.', size=20)
    phone=fields.Char()
    address=fields.Char()