# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class xmarts_cancelation_sales(models.Model):
#     _name = 'xmarts_cancelation_sales.xmarts_cancelation_sales'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100