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
    grade_id = fields.Many2one('material.grade', string = "Grade")
    order_id = fields.Many2one('mill.order', string="Order")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], string='Status', default='draft')

    def _select(self):
        select_str = """
            WITH mill_order_size_line_completed AS (select sum(completed_qty) as cq,line_id from  mill_order_size_line_completed GROUP BY line_id )  
            select
                ol.size as name,
                ol.partner_id,
                o.state,
                ol.order_qty as order_qty,
                ol.grade_id,
                COALESCE(olc.cq,0) AS completed_qty,
                ol.order_id,
                (ol.order_qty - COALESCE(olc.cq,0)) as balance

        """
        return select_str

    def _from(self):
        from_str = """
            mill_order_size_line as ol
		    INNER JOIN mill_order as o on ol.order_id = o.id
		    LEFT JOIN mill_order_size_line_completed as olc on olc.line_id = ol.id 
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
