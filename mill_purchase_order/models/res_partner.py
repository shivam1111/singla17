from odoo import models, fields,_


class ResPartner(models.Model):
    _inherit = "res.partner"

    def print_brokerage_report(self):
        return {
                'type': 'ir.actions.act_window',
                'name': _('Print Brokerage Report'),
                'res_model': 'brokerage.report',
                'target': 'new',
                'view_mode': 'form',
                'context': {'default_partner_id': self.id}, }

    is_broker = fields.Boolean('Broker')

