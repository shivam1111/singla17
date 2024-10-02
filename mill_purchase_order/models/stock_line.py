from odoo import api, fields, models, SUPERUSER_ID, _


class StockLine(models.Model):
    _name = "stock.line"
    _description = "Stock Line"
    _order = "date desc"



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.line') or _('New')
        result = super(StockLine, self).create(vals_list)
        return result

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        self.partner_id = self.purchase_id.partner_id

    def get_ttype_selection(self):
        res = []
        if self.env.context.get('default_type',False) == 'trade':
            res = [('adjustment','Adjustment Entry'),('trade','Trading')]
        else:
            res = [('production','Production'),('purchase','Purchase'),('adjustment','Adjustment Entry'),('trade','Trading')]
        return res

    name = fields.Char('Name',default = '/',required = True)
    date = fields.Date('Date',required=True,default = fields.Date.today)
    remarks = fields.Text('Remarks')
    partner_id = fields.Many2one('res.partner', help="Mostly furance, but depends on usage", string="Partner")
    grade_id = fields.Many2one('material.grade', string="Material Grade", required=True)
    type = fields.Selection(selection = get_ttype_selection,
                            string = "Type",help = "Determines the purpose for which the line has been created",required=True)
    qty = fields.Float('Qty')
    purchase_id = fields.Many2one('mill.purchase.order',string="Purchase Order")
    heat_ids = fields.One2many('heat.heat', 'stock_line_id','Heats')
    truck_no = fields.Char('Truck No.')
    bill_no = fields.Char("Bill No.")
    state = fields.Selection(selection=[('stock','Stock Updated'),('heats','Heats Updated')],
                             string = "State",default = "stock")
    trading_partner_id = fields.Many2one('res.partner', 'Partner')
