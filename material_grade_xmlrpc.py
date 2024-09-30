# import xmlrpclib

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
search_line_ids = data_model.execute_kw(database, uid, password, 'material.grade', 'search', [[['active', '=', True]]])
grade_data = ['name','name_str','color','active','line_ids']
data = data_model.execute_kw(database, uid, password, 'material.grade', 'read', [search_line_ids],{'fields':grade_data})


# Mapping Chemical Elements
chemical_element_ids = data_model.execute_kw(database, uid, password, 'chemical.element', 'search', [[]])
chemical_element_data1  = data_model.execute_kw(database, uid, password, 'chemical.element', 'read', [chemical_element_ids],{'fields':['name','code','display_name']})
df1 = pd.DataFrame(chemical_element_data1)

chemical_element_ids2 = data_model2.execute_kw(database, uid2, password2, 'chemical.element', 'search', [[]])
chemical_element_data2  = data_model2.execute_kw(database, uid2, password2, 'chemical.element', 'read', [chemical_element_ids2],{'fields':['name','code','display_name']})
df2 = pd.DataFrame(chemical_element_data2)


for grade in data:
    write_vals = {
        'name':grade.get('name'),
        'print_name':grade.get('name_str',False),
        'active':grade.get('active',False),
    }
    if grade.get('line_ids',False):
        lines = data_model.execute_kw(database, uid, password, 'composition.line', 'read', [grade.get('line_ids')])
        line_data = []
        for i in lines:
            q = df1.query("id==%s"%i.get('element_id')[0]).get('code').to_list()
            print(q)
            element_id = df2.query("code==%s"%q).get('id').to_list()
            print(element_id)
            line_data.append([
                0,0,{
                    'min_val':i.get('min_val',0),
                    'max_val':i.get('max_val',0),
                    'element_id':element_id[0]
                }
            ])
        write_vals.update({'line_ids':line_data})
    data_model2.execute_kw(database, uid2, password2, 'material.grade', 'create', [write_vals])