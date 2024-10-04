from odoo import tools
from odoo import api, fields, models


class MillOrderReport(models.Model):
    _name = "mill.order.report"
    _description = "Order Report"
    _auto = False

    name = fields.Many2one('size.size','Size')
    order_qty = fields.Float('Order Qty')
    completed_qty = fields.Float('Completed Qty')
    balance = fields.Float('Balance')
    partner_id = fields.Many2one('res.partner', string="Customer")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], string='Status', default='draft')

    def _select(self):
        select_str = """
            select 
                ol.size as name,
                avg(ol.order_qty) as order_qty,
                avg(o.completed_qty) as completed_qty,
                avg(o.order_qty - o.completed_qty)  as balance,
                ol.partner_id,
                o.state
        """
        return select_str

    def _from(self):
        from_str = """
            mill_order_size_line as ol INNER JOIN mill_order as o ON ol.order_id=o.id 
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY ol.partner_id,ol.size,o.state
        """
        return group_by_str

    def init(self):
        # self._table = mill_order_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s
            WHERE o.state = 'draft'
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

