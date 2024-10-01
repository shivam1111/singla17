from datetime import timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class MaterialFeature(models.Model):
    _name = "material.feature"
    _description = "Material Feature"

    name = fields.Char('Name',required=True)

class Size(models.Model):
    _name = "size.size"
    _description = "Flats Size"

    @api.depends("name")
    def _compute_display_name(self):
        for i in self:
            i.display_name =  i.name + " (" + i.corner_id.name + ")"

    name = fields.Char('Size', required=True)
    corner_id = fields.Many2one('corner.type', string="Corner Type", required=True)
    remarks = fields.Text('Remarks')


class CornerType(models.Model):
    _name = "corner.type"
    _description = "Corner Type"

    name = fields.Char('Name',required=True)


class IngotSize(models.Model):
    _name = "ingot.size"
    _description = "Ingot Size"

    name = fields.Char('Name',required=True)

class MillOrderSizeLine(models.Model):
    _name = "mill.order.size.line"
    _description = "Mill Order Size Line"
    _order = "sequence,id"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('display_type',False):
                vals['name'] = self.env['ir.sequence'].next_by_code('mill.order.size.line') or _('New')
            else:
                vals.update(size=self.env.ref('mill_order.data_size_unknown').id)
        result = super(MillOrderSizeLine, self).create(vals_list)
        return result

    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                _("You cannot change. Delete and recreate the line"))
        return super().write(values)

    @api.depends('size','name')
    def _compute_display_name(self):
        for line in self:
            if not line.display_type:
                line.display_name = "{ref}-{size}".format(**{'ref':line.name,'size':line.size.name})
            else:
                line.display_name = "Unassigned {}".format(line.id)

    name = fields.Char('Ref.')
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
        ],
        default=False)
    size = fields.Many2one('size.size')
    sequence = fields.Integer(string="Sequence")
    order_qty = fields.Float('Order Qty')
    rate = fields.Float("Rate")
    remarks = fields.Text("Remarks")
    corner_id = fields.Many2one('corner.type', string="Corner Type", related="size.corner_id", store=True)
    order_id = fields.Many2one('mill.order',ondelete='cascade', index=True, copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', related="order_id.partner_id", string="Customer", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], string='Status', copy=False, index=True, related="order_id.state")
    grade_id = fields.Many2one('material.grade', 'Grade')
    booking_date = fields.Date('Booking Date', default=fields.Date.today)
    cut_length = fields.Char('Cut Length')
    ingot_size = fields.Many2one('ingot.size', 'Ingot Size')

class MillOrderSizeLineCompleted(models.Model):
    _name = "mill.order.size.line.completed"
    _description = "Mill Order Size Line Completed"

    @api.onchange('line_id')
    def _onchange_line_id(self):
        if self.line_id and self.line_id.size:
            self.size_id =self.line_id.size

    @api.model_create_multi
    def create(self, vals):
        # vals is a list of dictionaries
        for i in vals:
            if i.get('name', _("New")) == _("New"):
                i['name'] = self.env['ir.sequence'].next_by_code('mill.order.size.line') or _('New')
        result = super(MillOrderSizeLineCompleted, self).create(vals)
        return result

    name = fields.Char('Ref',default=lambda self: _('New'))
    size_id = fields.Many2one('size.size',"Size")
    line_id = fields.Many2one('mill.order.size.line','Order Line')
    completed_qty = fields.Float('Qty')
    remarks = fields.Text("Remarks")
    invoice = fields.Char('Invoice No.')
    order_id = fields.Many2one('mill.order')
    complete_date = fields.Date('Date',default = fields.Date.today)

class MillOrder(models.Model):
    _name = "mill.order"
    _description = "Mill Order"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'mill.order', sequence_date=seq_date) or _("New")
        return super().create(vals_list)

    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    def set_state_done(self):
        self.state = 'done'

    @api.depends('rate','extra_rate','rolling')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            order.update({
                'net_rate': order.rate + order.extra_rate + order.rolling
            })

    @api.onchange('line_ids')
    def _onchange_order_qty(self):
        self.ensure_one()
        qty = sum(map(lambda x: x.order_qty, self.line_ids))
        self.order_qty = qty

    @api.depends('line_ids','line_ids.order_qty','line_completed_ids.completed_qty')
    def _compute_qty(self):
        '''
            Compute the total ordered and completed qty
        '''
        for order in self:
            complete_qty = sum(map(lambda x: x.completed_qty, order.line_completed_ids))
            order.completed_qty = complete_qty
            order.balance = self.order_qty - complete_qty

    def _compute_doc_count(self):
        Attachment = self.env['ir.attachment']
        for i in self:
            i.doc_count = Attachment.search_count([('res_model', '=','mill.order'), ('res_id', '=', i.id)])

    def attachment_tree_view(self):
        domain = ['&', ('res_model', '=', 'mill.order'), ('res_id', 'in', self.ids)]
        res_id = self.ids and self.ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'help': _('''<p class="oe_view_nocontent_create">Attach documents</p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}"
                       % (self._name, res_id)
        }

    # === FIELDS ===#
    name = fields.Char('Ref', default=lambda self: _('New'))
    size = fields.Char(string='Size', required=True, default="Size Unknown")
    order_qty = fields.Float('Quantity',required=True)
    partner_id = fields.Many2one('res.partner','Customer',required=True)
    note = fields.Text('Note')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_get_default_currency_id',
        store=True,
        precompute=True,
        ondelete='restrict'
    )
    rate = fields.Monetary('Basic Rate/MT', currency_field="currency_id")
    extra_rate = fields.Monetary('Extra Rate', currency_field="currency_id")
    rolling = fields.Monetary('Rolling',currency_field = "currency_id")
    net_rate = fields.Monetary(string='Net Rate', store=True, readonly=True,currency_field = "currency_id", compute='_amount_all')
    booking_date = fields.Date('Booking Date',default = fields.Date.today,required=True)
    delivery_date = fields.Date('Delivery Date')
    completed_qty = fields.Float('Completed', compute='_compute_qty',store=True)
    inclusive_loading = fields.Boolean('Loading Inclusive')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel','Cancel'),
        ], string='Status', readonly=False, copy=False, index=True, default='draft')
    line_ids = fields.One2many('mill.order.size.line','order_id','Order Lines')
    line_completed_ids = fields.One2many('mill.order.size.line.completed','order_id','Completed Order Lines')
    material_feature_ids = fields.Many2many('material.feature','mill_order_material_feature_rel','order_id','feature_id','Features')
    balance = fields.Float('Balance', compute='_compute_qty',store=True)
    doc_count = fields.Integer(compute="_compute_doc_count",string = "No. of Docs Attached")
    attachement_ids = fields.One2many('ir.attachment','res_id', string="Attachment")