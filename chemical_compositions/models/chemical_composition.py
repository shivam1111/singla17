from odoo import models, fields, api


class ProcessRoute(models.Model):
    _name = "process.route"
    _description = "Process Route"

    name = fields.Char('Route')

class InclusionRatingLine(models.Model):
    _name = "inclusion.rating.line"
    _description = "Inclusion Rating Line"

    type = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], string="Inclusion Type")
    thin = fields.Char('Thin')
    thick = fields.Char('Thick')
    composition_id = fields.Many2one('chemical.composition', 'Composition')


class CompositionLine(models.Model):
    _inherit = "composition.line"
    _description = "Chemical Composition Lines"

    composition_id = fields.Many2one('chemical.composition','Test Certificate')


class ChemicalComposition(models.Model):
    _name = "chemical.composition"
    _description = "Chemical Compositions"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('chemical.composition') or _('New')
        result = super(ChemicalComposition, self).create(vals)
        return result

    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        print('--------grade_id', self._context)
        if self.env.context.get('onchange_heat_id',False):
            return
        for c in self:
            data = []
            grade_id = c.grade_id
            c.line_ids.unlink() # Once executed change is grade_id is resetted. Hence we are saving the grade in previous line
            for i in grade_id.line_ids:
                data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val}))
            c.line_ids = data
            c.grade_id = grade_id

    @api.onchange('heat_id')
    def _onchange_heat_id(self):
        print('--------heat_id',self._context)
        for c in self:
            data = []
            heat_id = c.heat_id
            c.line_ids.unlink()
            for i in heat_id.line_ids:
                data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val,'furnace_val':i.furnace_val,'actual_val':i.actual_val}))
            c.line_ids = data
            c.grade_id = heat_id.grade_id
            c.heat_no = heat_id.name
            c.heat_id = heat_id

    @api.depends('line_ids','line_ids.element_id','line_ids.actual_val')
    def _compute_carbon_equivalence(self):
        for tc in self:
            ce = 0.00
            nicrmo = 0.00
            for l in tc.line_ids:
                if l.element_id.code == 'C':
                    ce += float(l.actual_val)
                if l.element_id.code == 'Mn':
                    ce += float(l.actual_val)/6.00
                if l.element_id.code == 'Ni':
                    nicrmo += float(l.actual_val)
                if l.element_id.code == 'Mo':
                    nicrmo += float(l.actual_val)
                if l.element_id.code == 'Cr':
                    nicrmo += float(l.actual_val)
            tc.carbon_equivalence = round (ce + 1.00/20.00,2)
            tc.nicrmo = round(nicrmo,2)

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Partner')
    no_of_pieces = fields.Float('Number of Pieces')
    date = fields.Date('Date',default = fields.Date.today)
    truck_no = fields.Char('Vehicle No.')
    heat_no = fields.Char('Heat No.')
    grade_id = fields.Many2one('material.grade','Grade')
    route_id = fields.Many2one('process.route','Process Route')
    heat_id = fields.Many2one('heat.heat', 'Select Heat No.')
    size = fields.Char('Size')
    color_code = fields.Char('Color Code')
    invoice_no = fields.Char('Invoice No.')
    line_ids = fields.One2many('composition.line','composition_id','Composition Line')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    inclusion_rating_ids = fields.One2many('inclusion.rating.line','composition_id','Inclusion Rating')
    min_hardness = fields.Char("Min. Hardness",default = "255")
    max_hardness = fields.Char("Max. Hardness",default = "280")
    complete_decarb = fields.Float('Complete Decarb')
    partial_decarb = fields.Float('Partial Decarb')
    grain_size = fields.Float('Grain Size')
    qty = fields.Char('Qty')
    ultimate_tensile_strength = fields.Float('Ultimate Tensile Strength (N/mm2)')
    yield_strength = fields.Float('Yield Strength (N/mm2)')
    elongation = fields.Float('Elongation %')
    reduction_ratio = fields.Char('Reduction Ratio')
    spark_test = fields.Boolean('Spark Test',default=False)
    is_xrf = fields.Boolean ('XRF Test',default=True)
    is_ut = fields.Boolean('UT Test')
    is_mpi = fields.Boolean('MPI')
    carbon_equivalence = fields.Float('Carbon Equivalence',default = 0.00,help = "%C + (%Mn/6) + 1/20",compute = '_compute_carbon_equivalence')
    nicrmo = fields.Float('Ni+Cr+Mo',compute = '_compute_carbon_equivalence')
    surface_inspection = fields.Selection([('ok','Ok'),('dentfree','Free from Dent')],default = 'dentfree')
    remarks = fields.Text("Remarks")

