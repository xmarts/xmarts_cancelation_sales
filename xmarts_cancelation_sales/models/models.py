# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_
from datetime import datetime, date, time, timedelta
import calendar

class SaleOrder(models.Model):
        _name = 'sale.order'
        _inherit = 'sale.order'

        state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('pagado', 'Pedido Pagado'),
        ('done', 'Locked'),
        ('entregado', 'Pedido Entregado'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

        #state_entregado = fields.Boolean(string='Pedido Entregado', default=False, compute='_compute_entregado')


        @api.multi
        def action_pagado(self):
                return self.write({'state': 'pagado'})

        @api.multi
        def comprobar_entregado(self):
                ent = True
                for l in self.order_line:
                        if l.product_uom_qty != l.qty_delivered:
                                ent = False
                if ent == True:
                        return self.write({'state': 'entregado'})
                else:
                        raise exceptions.ValidationError('Aun hay lineas por entregar.')


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