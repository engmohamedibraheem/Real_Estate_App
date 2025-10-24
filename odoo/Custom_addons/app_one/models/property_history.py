from email.policy import default

from dateutil.utils import today

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class PropertyHistory(models.Model):
    # Table by ORM
    _name = 'property.history'
    _description = 'Property History'

    # Create Fields as a Colum
    user_id=fields.Many2one('res.users')
    property_id=fields.Many2one('property')
    old_state=fields.Char()
    new_state=fields.Char()
    date_time=fields.Datetime(default=fields.Datetime.now,readonly=1)
    reason = fields.Char()

    def _compute_current_time(self):
        for rec in self:
            rec.date_time = fields.Datetime.now()