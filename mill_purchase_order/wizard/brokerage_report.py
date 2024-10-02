from odoo import models, fields,api

class ReportBrokerageReport(models.AbstractModel):
    _name = 'report.mill_purchase_order.template_brokerage_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.line'].browse(data.get('doc_ids',[]))
        data.update(
            {

            'docs':docs,

             })
        # return a custom rendering context
        return data


class BrokerageReport(models.TransientModel):
    _name = 'brokerage.report'
    _description = "Brokerage Report"

    def print_report(self):
        stock_line = self.env['stock.line'].search([('purchase_id.broker_id','=',self.partner_id.id),
                                                    ('date','>=',self.from_date),
                                                    ('date','<=',self.to_date),
                                                    ('purchase_id.state','!=','cancel'),
                                                    ('type','in',['purchase','trade']),
                                                    ])
        data = {
            'doc_ids': stock_line.ids,
            'broker_name': self.partner_id.name,
            'print_basic_rate':self.show_basic_price
        }
        report = self.env.ref('mill_purchase_order.action_brokerage_report')
        return report.report_action(self,data=data,config=False)



    partner_id = fields.Many2one('res.partner','Broker',required=True)
    from_date = fields.Date(string="From Date",default=fields.Date.to_date('2024-09-01'))
    to_date = fields.Date(string = "To Date",default=fields.Date.to_date('2024-09-20'))
    show_basic_price = fields.Boolean('Show Basic Price ?')
