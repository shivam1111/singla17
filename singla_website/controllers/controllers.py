# -*- coding: utf-8 -*-
# from odoo import http


# class SinglaWebsite(http.Controller):
#     @http.route('/singla_website/singla_website', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/singla_website/singla_website/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('singla_website.listing', {
#             'root': '/singla_website/singla_website',
#             'objects': http.request.env['singla_website.singla_website'].search([]),
#         })

#     @http.route('/singla_website/singla_website/objects/<model("singla_website.singla_website"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('singla_website.object', {
#             'object': obj
#         })

