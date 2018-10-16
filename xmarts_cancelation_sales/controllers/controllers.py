# -*- coding: utf-8 -*-
from odoo import http

# class XmartsCancelationSales(http.Controller):
#     @http.route('/xmarts_cancelation_sales/xmarts_cancelation_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xmarts_cancelation_sales/xmarts_cancelation_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xmarts_cancelation_sales.listing', {
#             'root': '/xmarts_cancelation_sales/xmarts_cancelation_sales',
#             'objects': http.request.env['xmarts_cancelation_sales.xmarts_cancelation_sales'].search([]),
#         })

#     @http.route('/xmarts_cancelation_sales/xmarts_cancelation_sales/objects/<model("xmarts_cancelation_sales.xmarts_cancelation_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xmarts_cancelation_sales.object', {
#             'object': obj
#         })