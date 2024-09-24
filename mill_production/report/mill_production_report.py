from odoo import models, fields, api

class MillProductionReport(models.AbstractModel):
    _name = 'report.mill_production.mill_production_report'  # report_name in xml
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Mill Production Report'

    def generate_xlsx_report(self, workbook, data, production_order):
        if len(self) == 1:
            print ("======There is only one object")
        else:
            for obj in production_order:
                print("--------obj",obj.name,data)
                report_name = obj.name
                # One sheet by partner
                sheet = workbook.add_worksheet(report_name[:31])
                bold = workbook.add_format({'bold': True})
                sheet.write(0, 0, obj.name, bold)