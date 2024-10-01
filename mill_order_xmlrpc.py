import xmlrpc.client
import pandas as pd

data_url = "http://www.singlasteel.in" # odoo instance url
database = 'ssai' # database name
user = 'admin' # username
password = 'Sale1989!' # api key
common_auth = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(data_url))
uid = common_auth.authenticate(database, user, password, {})

data_url2 = "http://52.66.18.249:8069" # odoo instance url
password2  = "d1995fb6b8af84731b4ea2172041d7ca01d8e907"
user2 = 'info@singlasteel.in' # username
common_auth2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(data_url2))
uid2 = common_auth2.authenticate(database, user2, password2, {})

data_model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(data_url))
data_model2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(data_url2))
# contacts = data_model2.execute_kw(database, uid2, password2, 'res.partner', 'search_read',  [[['active', '=', True]]])
# db_contacts = pd.DataFrame(contacts)

order_ids = data_model.execute_kw(database, uid, password, 'mill.order', 'search', [[['state', '=', 'draft']]])
incomplete = []
for i in order_ids:
    order_data = data_model.execute_kw(database, uid, password, 'mill.order', 'read', [i]).pop() #Substituted i
    partner_id = data_model2.execute_kw(database, uid2, password2, 'res.partner', 'search', [[['name', '=', order_data.get('partner_id')[1]]]])
    if partner_id:
        vals ={
            'partner_id':partner_id[0],
            'rate':order_data.get('rate'),
            'extra_rate':order_data.get('extra_rate'),
            'rolling':order_data.get('rolling'),
            'order_qty':order_data.get('order_qty'),
            'inclusive_loading': order_data.get('inclusive_loading'),
            'booking_date': order_data.get('booking_date'),
            'size': order_data.get('size'),
            'completed_qty': order_data.get('completed_qty'),
            'balance': order_data.get('balance'),
        }
        line_data = data_model.execute_kw(database, uid, password, 'mill.order.size.line', 'read', [order_data.get('line_ids')])
        line_data_new = []
        for line in line_data:
            grade_id = data_model2.execute_kw(database, uid2, password2, 'material.grade', 'search', [[['name', '=', line.get('grade_id')[1]]]])
            size_name = data_model.execute_kw(database, uid, password, 'size.size', 'read', [line.get('name')[0]],{'fields':['name']}).pop()
            size_id = data_model2.execute_kw(database, uid2, password2, 'size.size', 'search', [[['name', '=', size_name.get('name')]]])
            line_data_new.append([
                0,0,{
                    'booking_date':order_data.get('booking_date'),
                    'partner_id':partner_id[0],
                    'rate':line.get('rate'),
                    'order_qty':line.get('order_qty'),
                    'grade_id':grade_id[0],
                    'size':size_id[0],
                    'cut_length':line.get('cut_length'),
                    'state':'draft',
                }
            ])
        vals.update({'line_ids':line_data_new})
        line_completed_data = data_model.execute_kw(database, uid, password, 'mill.order.size.line.completed', 'read', [order_data.get('line_completed_ids')])
        print(line_completed_data)
        line_completed_data_new = []
        for l in line_completed_data:
            if l.get('size_id',False):
                size_name = data_model.execute_kw(database, uid, password, 'size.size', 'read', [l.get('size_id')[0]],
                                                  {'fields': ['name']}).pop()

                size_id = data_model2.execute_kw(database, uid2, password2, 'size.size', 'search',
                                                 [[['name', '=', size_name.get('name')]]])
            else:
                size_id=False
            line_completed_data_new.append([
                0,0,{
                    'size_id':size_id and size_id[0] or False,
                    'completed_qty':l.get('completed_qty'),
                    'invoice':l.get('invoice'),
                    'remarks':l.get('remarks'),
                    'complete_date':l.get('complete_date'),
                }
            ])
        vals.update({'line_completed_ids': line_completed_data_new})
        data_model2.execute_kw(database, uid2, password2, 'mill.order', 'create', [vals])
    else:
        incomplete.append(i)
print("Incomplete:",incomplete)