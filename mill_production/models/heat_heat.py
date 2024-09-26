from odoo import models, fields, api

class Heat(models.Model):
    _inherit = "heat.heat"
    _description = "Attach Production"

    def _get_production_lines(self):
        for heat in self:
            heat.stock_line_ids = self.env['stock.line'].search([('heat_no_ids','in',heat.id)])

    stock_line_ids = fields.Many2many('stock.line',string = "Production",compute = "_get_production_lines")