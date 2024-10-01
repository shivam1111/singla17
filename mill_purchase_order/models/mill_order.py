from odoo import models, fields, api

class MillOrder(models.Model):
    _inherit="mill.order"
    _description = "Mill Order with PO"

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        for so in self:
            if so.purchase_id:
                so.rate = so.purchase_id.net_rate

    purchase_id = fields.Many2one('mill.purchase.order','Purchase Order')