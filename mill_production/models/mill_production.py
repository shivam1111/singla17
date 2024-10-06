from odoo import models, fields, api
class StockLine(models.Model):
    _inherit ="stock.line"
    _description = "Attaching Production to Stocl Lines"

    @api.onchange('pcs', 'kg_per_pc')
    def _compute_qty(self):
        for line in self:
            line.qty = -(line.kg_per_pc * line.pcs) / 1000

    @api.depends('scrap', 'qty')
    def _compute_scrap(self):
        for line in self:
            try:
                line.scrap_percentage = (line.scrap * 100) / (1000 * line.qty)
            except ZeroDivisionError:
                line.scrap_percentage = 0.00

    name = fields.Char('Name')
    pcs = fields.Float('Pcs')
    sequence = fields.Integer('sequence', help="Sequence for the handle.",default=10)
    size_id = fields.Many2one('size.size',string  = "Size")
    batch = fields.Float('No. of Batch',help = "Dhakku")
    kg_per_pc = fields.Float('Kg/pc')
    production_id = fields.Many2one('mill.production','Production',ondelete='cascade')
    scrap = fields.Float('Scrap')
    scrap_percentage = fields.Float('Scrap%',compute = "_compute_scrap",digits=(16, 2))
    heat_no_ids = fields.Many2many('heat.heat','stock_line_heat_heat_relation','stock_line_id','heat_id','Heats')
    production_line_id = fields.Many2one('production.order.line', 'Prooduction Line', help="This field stores the planned productio line")

class MillProduction(models.Model):
    _name = 'mill.production'
    _description = "Mill Production Register"

    def write(self, vals):
        if self.env.user.has_group('mill_order.group_dispatch_manager') and self.env.user.id != SUPERUSER_ID:
            raise UserError(_('You are not allowed to make changes to this record'))
        return super(MillProduction, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.user.has_group('mill_order.group_dispatch_manager') and self.env.user.id != SUPERUSER_ID:
                raise UserError(_('You are not allowed to create this record'))
            vals['name'] = self.env['ir.sequence'].next_by_code('mill.production') or _('New')

        return  super(MillProduction, self).create(vals_list)

    @api.depends('total_production', 'production_line_ids.scrap')
    def _compute_scrap(self):
        for po in self:
            total = 0.00
            for i in po.production_line_ids:
                total = total + i.scrap
            po.total_scrap = total

    @api.depends('total_production', 'production_line_ids.scrap')
    def _compute_scrap_percentage(self):
        for po in self:
            try:
                po.scrap_percentage = (po.total_scrap * 100) / (1000 * po.total_production)
            except ZeroDivisionError:
                po.scrap_percentage = 0.00

    @api.depends('production_line_ids', 'production_line_ids.qty','hours')
    def _compute_total_production(self):
        for po in self:
            total = 0.00
            for i in po.production_line_ids:
                total = total + i.qty
            po.total_production = -total
            try:
                po.production_mt = total/po.hours
            except ZeroDivisionError:
                po.production_mt = 0.0

    @api.depends('kwh_closing','kwh_opening','total_production')
    def _compute_units(self):
        for po in self:
            po.total_units = (po.kwh_closing - po.kwh_opening)*15
    @api.depends('kwh_closing','kwh_opening','total_production')
    def _compute_units_mt(self):
        for po in self:
            try:
                po.units_per_mt = po.total_units / po.total_production
            except ZeroDivisionError:
                po.units_per_mt = 0.00

    @api.depends('total_production', 'production_line_ids.scrap')
    def _compute_kwh_mt(self):
        for po in self:
            try:
                po.kwh_mt = po.total_units / po.total_production
            except ZeroDivisionError:
                po.kwh_mt = 0.00

    @api.depends('png_units_opening', 'png_units_closing')
    def _compute_png_units(self):
        for po in self:
            po.png_net = po.png_units_closing - po.png_units_opening

    @api.depends('png_units_opening', 'png_units_closing')
    def _compute_png_mt(self):
        for po in self:
            try:
                po.png_net_mt = po.png_net/po.total_production
            except ZeroDivisionError:
                po.png_net_mt = 0.00
    @api.depends('solar_units_opening_kwh','solar_units_closing_kwh')
    def _compute_solar_production(self):
        for po in self:
            po.solar_net = po.solar_units_closing_kwh - po.solar_units_opening_kwh

    name = fields.Char('Name', default='/', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    total_production = fields.Float('Total Production', compute="_compute_total_production", store=True)
    production_mt = fields.Float('Production Rate',compute="_compute_total_production",digits=(16, 2))
    remarks = fields.Text('Remarks')
    production_line_ids = fields.One2many('stock.line', 'production_id', 'Production Lines')
    md_mt = fields.Float('MD/MT')
    total_scrap = fields.Float('Total Scrap', compute="_compute_scrap", store=True)
    scrap_percentage = fields.Float('Scrap%', compute="_compute_scrap_percentage")
    hours = fields.Float('Total Hours')
    furnace_kara = fields.Float('Furnace Kara')
    mill_kara = fields.Float('Mill Kara')
    miss_roll = fields.Text('Miss Roll')
    total_units = fields.Float("Total Units Consumed", compute="_compute_units", store=True)
    units_per_mt = fields.Float('Units/MT', compute='_compute_units_mt',digits=(16, 2))
    kwh_mt = fields.Float('KWH/MT', compute='_compute_kwh_mt')
    size_id = fields.Many2one('size.size', related="production_line_ids.size_id", string="Size")
    water_units_opening = fields.Float('Water Units Opening')
    water_units_closing = fields.Float('Water Units Closing')
    solar_units_opening_kwh = fields.Float('Solar Units Opening (KWH)')
    solar_units_closing_kwh = fields.Float('Solar Units Closing (KWH)')
    solar_net = fields.Float('Solar Production', compute='_compute_solar_production',store=True)
    solar_units_opening_kvah = fields.Float('Solar Units Opening (KVaH)')
    solar_units_closing_kvah = fields.Float('Solar Units Closing (KVaH)')
    png_units_opening = fields.Float('PNG Opening')
    png_units_closing = fields.Float('PNG Closing')
    kwh_opening = fields.Float('KWH Op.')
    kwh_closing = fields.Float('KWH Cl.')
    kva_opening = fields.Float('KVA Op.')
    kva_closing = fields.Float('KVA Cl.')
    png_net = fields.Float("Total PNG", compute='_compute_png_units', store=True)
    png_net_mt = fields.Float('PNG (SCM/MT)',compute="_compute_png_mt",digits=(16, 2))
    order_id = fields.Many2one('production.order', 'Production Order')