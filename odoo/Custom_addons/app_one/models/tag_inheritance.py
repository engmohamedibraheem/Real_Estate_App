from odoo import models

class TagInherit(models.Model):

    _inherit = 'tag'
    _name = 'tag.inherit'
