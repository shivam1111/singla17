from odoo import models, fields, api

class MillProductionReport(models.AbstractModel):
    _name = 'report.mill_production.mill_production_report'  # report_name in xml
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Mill Production Report'

    def generate_xlsx_report(self, workbook, data, po):
        headers_row = ['Size','Net Wt','Scrap','Scrap %']
        summary_headers = ['','Water','Solar (KW)','Solar (KV)','KW','KV']

        if len(self) <= 1:
            def write_row(sheet,column,counter,row,format):
                sheet.write_row('{column}{row}'.format(column=column,row=counter),row,format)
                return counter+1

            report_name = po.name
            sheet = workbook.add_worksheet(report_name[:31])
            header_format = workbook.add_format({'bold': True})
            header_format.set_border()
            header_format.set_align('center')
            col_header_format = workbook.add_format({'bold': True,'border':1})
            col_format = workbook.add_format({'border':1})
            row_counter = 1
            date_format = workbook.add_format({'num_format': 'dd/mm/yy','bold':True,'border':1})
            date_format.set_align('center')
            date_row = ['Date',po.date]
            col_counter = len(headers_row)
            #Adding Water Column
            sheet.write_column(row_counter+1,col_counter,['Op.','Cl.','Net'],col_header_format)
            col_counter+=1
            col_format.set_bold(False)
            sheet.write_column(row_counter+1,col_counter,[po.water_units_opening,po.water_units_closing,(po.water_units_closing-po.water_units_opening)],col_format)
            col_counter+=1
            sheet.write_column(row_counter + 1, col_counter, [po.solar_units_closing_kwh, po.solar_units_opening_kwh,
                                                              (po.solar_units_closing_kwh - po.solar_units_opening_kwh)],col_format)
            col_counter += 1
            sheet.write_column(row_counter + 1, col_counter, [po.solar_units_opening_kvah, po.solar_units_closing_kvah,
                                                              (po.solar_units_closing_kvah - po.solar_units_opening_kvah)],col_format)
            col_counter += 1
            sheet.write_column(row_counter + 1, col_counter, [po.kwh_opening, po.kwh_closing,
                                                              (po.kwh_closing - po.kwh_opening)],col_format)

            col_counter += 1
            sheet.write_column(row_counter + 1, col_counter, [po.kva_opening, po.kva_closing,
                                                              (po.kva_closing - po.kva_opening)],col_format)

            row_counter = write_row(sheet,'A',row_counter,date_row,date_format)
            row_counter  = write_row(sheet,'A',row_counter,headers_row+summary_headers,header_format)
            for i,line in enumerate(po.production_line_ids):
                row_format = workbook.add_format()
                row_format.set_align('center')
                row_format.set_border()
                row = [
                       line.size_id.name,line.qty,
                       line.scrap,
                       line.scrap_percentage,
                   ]
                sheet.write_row('A%s' % row_counter, row,row_format)
                row_counter+=1
            # Summary Printing
            summary_row = ['PNG/MT',po.png_net_mt,'MD/MT',po.md_mt,'Hours',po.hours,'Units/MT',po.units_per_mt]
            summary_format = workbook.add_format({'bold':True})
            summary_format.set_border()
            summary_format.set_align('center')
            row_counter = write_row(sheet,'A',row_counter,summary_row,summary_format)

        else:
            for obj in po:
                report_name = obj.name
                sheet = workbook.add_worksheet(report_name[:31])
                bold = workbook.add_format({'bold': True})
                sheet.write(0, 0, obj.name, bold)