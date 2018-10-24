# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import models, fields, api, exceptions,_
from datetime import datetime, date, time, timedelta
import calendar

class TimeCancelationSales(models.Model):
        _name='time.cancelation.sale'

        name = fields.Char(string='Descripción')
        horas = fields.Integer(string='Tiempo para cancelacion (Horas)')

class ResConfigSettings(models.Model):
        _inherit = "res.company"

        time_to_cancel = fields.Many2one('time.cancelation.sale',string="Tiempo para cancelacón de ventas")

class SaleOrderAutoCancel(models.Model):
        _name = 'sale.order'
        _inherit = 'sale.order'

        cancelacion_automatica = fields.Datetime(string="Fecha de cancelacion automatica", compute="action_cancelacion_automatica")
        state_cancel = fields.Selection([
        ('not_payed', 'Sin Pagar'),
        ('payed', 'Pagado'),
        ('delivered', 'Entregado'),
        ('cancel', 'Cancelado por tiempo')], string='Estado del pedido', readonly=True, default='not_payed')

        @api.one
        @api.multi
        def action_cancelacion_automatica(self):
                DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                if self.confirmation_date and self.payment_term_id.id == 1 and self.state_cancel == 'not_payed':
                        fc = self.confirmation_date
                        fechahora = datetime.strptime(fc, DATETIME_FORMAT)
                        horas = int(self.company_id.time_to_cancel.horas)
                        fechahora = fechahora + timedelta(hours=horas)
                        self.cancelacion_automatica = fechahora
                        if self.state == 'sale': 
                                if datetime.now() > fechahora:
                                        if self.picking_ids:
                                                for p in self.picking_ids:
                                                        if p.state in ['waiting','confirmed','assigned']:
                                                                for m in p.move_lines:
                                                                        cr = self.env.cr
                                                                        sql = "update stock_move set state='cancel' where id='"+str(m.id)+"'"
                                                                        cr.execute(sql)
                                                                for ml in p.move_line_ids:
                                                                        cr = self.env.cr
                                                                        sql = "update stock_move_line set state='cancel',product_uom_qty='0',product_qty='0' where id='"+str(ml.id)+"'"
                                                                        cr.execute(sql)
                                                                cr = self.env.cr
                                                                sql = "update stock_picking set state='cancel' where id='"+str(p.id)+"'"
                                                                cr.execute(sql)
                                        self.write({'state_cancel': 'cancel'})
                                        cr = self.env.cr
                                        sql = "update sale_order set state='cancel', invoice_status='no' where id='"+str(self.id)+"'"
                                        cr.execute(sql)
                else:
                        self.cancelacion_automatica = ''
                        if self.state_cancel == 'cancel' and self.state == 'sale':
                                self.write({'state_cancel': 'not_payed'})
                ent = True
                for l in self.order_line:
                        if l.product_uom_qty != l.qty_delivered:
                                ent = False
                if ent == True:
                        self.write({'state_cancel': 'delivered'})

        @api.multi
        def action_pagado(self):
                return self.write({'state_cancel': 'payed'})


class ResConfigSettings(models.TransientModel):
        _inherit = "res.config.settings"

        time_to_cancel = fields.Many2one('time.cancelation.sale',string="Tiempo para cancelacón de ventas", related='company_id.time_to_cancel')


class AutoCancelStockPicking(models.Model):
        _name = "stock.picking"
        _inherit = 'stock.picking'

        sale_state = fields.Selection([
        ('not_payed', 'Sin Pagar'),
        ('payed', 'Pagado'),
        ('delivered', 'Entregado'),
        ('cancel', 'Cancelado por tiempo')], string='Estado del pedido', readonly=True, related='sale_id.state_cancel')

        @api.multi
        def button_validate(self):
                self.ensure_one()
                if self.sale_id:
                        if self.sale_id.state_cancel != 'payed' and self.sale_id.payment_term_id.id == 1:
                                raise exceptions.ValidationError('Orden sin pagar')
                        else:
                                res = super(AutoCancelStockPicking, self).button_validate()
                                return res
                else:
                        res = super(AutoCancelStockPicking, self).button_validate()
                        return res

