from email.policy import default

from dateutil.utils import today

from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Property(models.Model):
    #Table by ORM
    _name='property'

    #Create Fields as a Colum
    name=fields.Char(required=1,default='ex: Mahmoud',size=20)
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(default=today())
    expected_price=fields.Float(required=1,digits=(0,5))
    selling_price=fields.Float()
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')],default='north')

    #Data base Tier validation
    _sql_constraints = [
        ('unique_name','unique("name")','This name is exist!')
    ]

    #logic Validation
    @api.constrains('expected_price')
    def _check_expected_price_equal_zero(self):
        for rec in self:
            if rec.expected_price == 0:
                raise ValidationError('please add valid number of expected price')

    #CURD Operation Methods
    @api.model_create_multi
    def create(self ,vals):
        res = super(Property,self).create(vals)
        print("inside create method")
        return res