from odoo import tools
from odoo import api, fields, models


class MillOrderReport(models.Model):
    _name = "mill.order.report"
    _description = "Order Report"
    _auto = False

    name = fields.Many2one('size.size', 'Size')
    order_qty = fields.Float('Order Qty')
    completed_qty = fields.Float('Completed Qty')
    balance = fields.Float('Balance')
    partner_id = fields.Many2one('res.partner', string="Customer")
    grade_id = fields.Many2one('material.grade',string = "Grade")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], string='Status', default='draft')

    def _select(self):
        select_str = """
            select
                ol.size as name,
                ol.partner_id,
                o.state,
                ol.order_qty as order_qty,
                ol.grade_id,
               COALESCE((select sum(completed_qty) from  mill_order_size_line_completed as olc where ol.id = olc.line_id ),0) as completed_qty,
                ol.order_qty - COALESCE((select sum(completed_qty) from  mill_order_size_line_completed as olc where ol.id = olc.line_id ),0) as balance

        """
        return select_str

    def _from(self):
        from_str = """
            mill_order_size_line as ol INNER JOIN mill_order as o on o.id = ol.order_id 
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY ol.size,ol.partner_id,o.state,ol.grade_id
        """
        return group_by_str

    def init(self):
        # self._table = mill_order_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s
            WHERE o.state = 'draft'
            )""" % (self._table, self._select(), self._from()))
