from odoo import models,fields,api

class Tag(models.Model):
    #Table by ORM
    _name='tag'
    name=fields.Char()