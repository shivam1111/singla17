#    Author: Guewen Baconnier
#    Copyright 2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api

class MaterialGrade(models.Model):
    _inherit = 'material.grade'

    @api.depends('stock_line_ids', 'stock_line_ids.qty')
    def _compute_qty(self):
        for grade in self:
            total = 0.00
            for i in grade.stock_line_ids:
                if i.type != 'trade':
                    total += i.qty
            grade.qty = total

    qty = fields.Float('Qty', compute="_compute_qty", store=True)
    stock_line_ids = fields.One2many('stock.line', 'grade_id', 'Stock')
    print_name = fields.Char('Print Name')
    line_ids = fields.One2many('composition.line', 'grade_id', 'Composition Line')
    remarks = fields.Text('Remarks')
