from odoo import models,fields,api

class AccountMove(models.Model):
    _inherit = 'account.move'

    property_id=fields.Many2one('property' , string="Property")

    def action_post(self):
        res=super(AccountMove,self).action_post()
        print("Inside action_post Method for inherit")
        return res
