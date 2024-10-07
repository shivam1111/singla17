from odoo import models, fields, api

class MillOrderSizeLine(models.Model):
    _inherit = "mill.order.size.line"
    _description = "Mill Order Size Line"

    def shift_to_production_plan(self):
        for line in self:
            if line.size and line.order_id:
                self.env['production.plan'].create({
                    'partner_id':line.order_id.partner_id.id,
                    'size_id':line.size.id,
                    'grade_id':line.grade_id.id,
                    'line_id':line.id,
                    'order_qty':line.order_qty,
                })
        return True

class ProductionPlan(models.Model):
    _name = "production.plan"
    _description = "Helps in Production Planning"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('production.plan') or _('New')
        result = super(ProductionPlan, self).create(vals)
        return result

    name = fields.Char('Code',default='/')
    sequence = fields.Integer(string="Sequence")
    date = fields.Date('Date',required=True,default = fields.Date.today)
    size_id = fields.Many2one('size.size','Size')
    partner_id = fields.Many2one('res.partner','Customer',required=True)
    line_id = fields.Many2one('mill.order.size.line','Order Line')
    order_id = fields.Many2one('mill.order',related='line_id.order_id',string = "Order")
    order_qty = fields.Float('Qty')
    corner_id = fields.Many2one('corner.type',related = 'size_id.corner_id',string = "Corner Type")
    grade_id  = fields.Many2one('material.grade',string = "Grade")