import xmlrpc.client
import pandas as pd

# ssh -i ~/ec2_keys/singla.pem ubuntu@52.66.18.249
# Sale1989!

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

po_name = ['SSAI-PO7557','SSAI-PO7563']
partner_id = 480
broker_id = 453
# Sanjay = 460
#Manojji = 453
#Rajenderji = 457

grade_id = 188
#sup9 = 65
#en8d = 71
#30mncrB5 = 98
#52100 = 188

po_ids = data_model.execute_kw(database, uid, password, 'mill.purchase.order', 'search',[[['name', 'in', po_name]]])
data_po = data_model.execute_kw(database, uid, password, 'mill.purchase.order', 'read',[po_ids])
for po in data_po:
    vals = {
        'partner_id':partner_id,
        'broker_id':broker_id,
        'date_order':po.get('date_order'),
        'heats':po.get('heats'),
        'material_ordered':po.get('material_ordered'),
        'basic_rate':po.get('basic_rate'),
        'grade_id':grade_id,
        'extra_rate':po.get('extra_rate'),
        'net_rate':po.get('net_rate'),
        'state':po.get('state'),
        'balance':po.get('balance'),
        'name':po.get('name'),
    }
    stock_lines = []
    if po.get('stock_line_ids',False):
        data_stock_line= data_model.execute_kw(database, uid, password, 'stock.line',
                                               'read',[po.get('stock_line_ids',[])])
        print(data_stock_line)
        for line in data_stock_line:
            stock_vals = {
                'qty':line.get('qty',0),
                'date':line.get('date'),
                'partner_id':partner_id,
                'bill_no':line.get('bill_no'),
                'truck_no':line.get('truck_no'),
                'state':'stock',
                'type':line.get('type'),
                'grade_id':grade_id,

            }
            stock_lines.append([0,0,stock_vals])
    vals.update({
        'stock_line_ids':stock_lines,
    })
    data_model2.execute_kw(database, uid2, password2, 'mill.purchase.order', 'create', [vals])