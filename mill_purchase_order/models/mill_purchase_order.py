from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

# TODO: Add Attachment to Purchase Order

class MillPurchaseOrder(models.Model):
    _name = "mill.purchase.order"
    _description = "Mill Purchase Order"
    _order = ['date_order','name']

    @api.depends('basic_rate','extra_rate')
    def _amount_all(self):
        """
        Compute the Net Rate
        """
        for order in self:
            order.update({
                'net_rate': order.basic_rate + order.extra_rate
            })

    @api.onchange('heats')
    def _onchage_heats(self):
        self.material_ordered = float(self.heats*7.50)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('mill.purchase.order') or _('New')
        result = super(MillPurchaseOrder, self).create(vals_list)
        return result

    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id


    @api.depends('stock_line_ids','material_ordered')
    def _compute_qty(self):
        for po in self:
            total = 0.00
            for i in po.stock_line_ids:
                total = total + i.qty
            self.material_received  = total
            balance = po.material_ordered - total
            self.balance = max(balance,0)



    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Supplier')
    date_order = fields.Date(string='Order Date', required=True, index=True, copy=False, default=fields.Date.today)
    grade_id = fields.Many2one("material.grade",'Grade')
    broker_id = fields.Many2one('res.partner','Broker',domain = [('is_broker','=',True)])
    size = fields.Many2one('ingot.size','Material Size')
    grade_id = fields.Many2one('material.grade','Material Grade')
    material_ordered = fields.Float('Material Qty Ordered')
    material_received = fields.Float('Material Qty Received')
    state = fields.Selection([
        ('order_placed', 'Order Placed'),
        ('done', 'Done'),
        ('cancel','Cancelled')
        ], string='Status', readonly=False, copy=False, index=True,  default='order_placed')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',default=_get_default_currency_id)
    basic_rate = fields.Monetary('Basic Rate',currency_field = "currency_id")
    extra_rate = fields.Monetary('Extra Rate',currency_field = "currency_id")
    stock_line_ids = fields.One2many('stock.line', 'purchase_id', 'Stock', domain=[('type', '=', 'purchase')])
    net_rate = fields.Monetary(string='Net Rate', store=False, readonly=True,currency_field = "currency_id", compute='_amount_all')
    material_feature_ids = fields.Many2many('material.feature','mill_purchase_order_material_feature_rel','order_id','feature_id','Features')
    heats= fields.Float('Heats')
    material_received = fields.Float('Material Qty Received', compute="_compute_qty", store=True)
    balance = fields.Float('Balance', compute="_compute_qty",store=True)