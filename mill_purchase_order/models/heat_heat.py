from odoo import models, fields, api
from odoo.tools.translate import _


class ChemicalElement(models.Model):
    _name = "chemical.element"
    _description = "Chemical Element"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)


class CompositionLine(models.Model):
    _name = "composition.line"
    _description = "Composition Line"

    element_id = fields.Many2one('chemical.element', 'Element', required=True)
    min_val = fields.Char('Min')
    max_val = fields.Char('Max')
    actual_val = fields.Char('Actual')
    furnace_val = fields.Char('Furnace Report')
    sequence = fields.Integer('Sequence')
    heat_id = fields.Many2one('heat.heat',string = 'Heat',ondelete='cascade', index=True, copy=False, readonly=True)
    grade_id = fields.Many2one('material.grade',"Grade")

class Heat(models.Model):
    _name = 'heat.heat'
    _description = "Heats"

    def print_heat_report(self):
        return self.env.ref('mill_purchase_order.action_heat_report').report_action(self)

    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        data = []
        line_ids = []
        # First check if the record is being created or grade_id value if being changed
        if self._context.get('onchange',False):
            # This means the grade_id field value is being changed
            line_ids = self.grade_id and self.grade_id.line_ids or []
        elif self.grade_id:
            line_ids = self.grade_id.line_ids
        for i in line_ids:
            data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val}))
        self.line_ids = data

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100,order=None):
        args = list(args or [])
        if name:
            args += ['|',('name',operator,name),('furnace_heat_no',operator,name)]
        return self._search(args, limit=limit, order=order)
        
    @api.depends('furnace_heat_no','name')
    def _compute_display_name(self):
        for heat in self:
            heat.display_name = "[" + str(heat.furnace_heat_no or "") + "]" + ' ' + heat.name



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('heat.heat') or _('New')
        result = super(Heat, self).create(vals_list)
        return result
        
    
    name = fields.Char('Internal Heat No.',default = '/',required = True)
    furnace_heat_no = fields.Char('Supplier Heat No.',required = True)
    grinding = fields.Boolean('Grinding')
    date = fields.Char('Date Rcvd',required=True,default = fields.Date.today)
    truck_no = fields.Char('Truck No.',related = "stock_line_id.truck_no",readonly=False)
    partner_id = fields.Many2one(string = " Supplier",related = "stock_line_id.partner_id",store=True,readonly=False)
    stock_line_id = fields.Many2one('stock.line','Stock Line')
    purchase_id = fields.Many2one('mill.purchase.order','Purchase Order',related = "stock_line_id.purchase_id")
    grade_id = fields.Many2one(string = "Grade",store=True,related = "stock_line_id.grade_id",readonly=False)
    line_ids = fields.One2many('composition.line','heat_id','Chemical Composition Report')
    surface_inspection = fields.Boolean('Surface Inspection')
    xrf_tested = fields.Boolean('XRF Tested')
    remarks = fields.Text('Remarks')
    state = fields.Selection(selection=[('ok','OK'),
                                        ('rejected','Rejected'),
                                        ('non_confirmance','Non Confirmance')],default='ok')
    size = fields.Many2one('ingot.size','Ingot Size')
    supervisor_id = fields.Many2one('res.users','Supervisor',default = lambda self:self.env.user)
    roll_size = fields.Many2many('size.size', string="Rolling Size", help="Rolling Size")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    print_supplier = fields.Boolean('Print Supplier',default=False)
    