import xmlrpc.client

url = "http://localhost:8069"  
db = 'db_civil'
username = 'admin'
password = 'admin'


common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
print("Authentication successful, UID:", uid)


'xmlrpc/2/object' 'execute_kw'
'db,uid,password,model_name,methods,[],{}'

patient_data = {
    'patient_name': 'test patient1',  
    'gender': 'male',           
    'contact': '+91 8780085668', 
    'date_of_birth': '1990-01-01', 
    'email_id': 'test@gmail.com.com', 


}
patient_id = 168
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

#Create Operation
# patient_ids = models.execute_kw(db,uid,password,"hospital.patient","create",[patient_data])
# print(patient_data)


# read operation 
# patient_data = models.execute_kw(
#     db, uid, password,
#     'hospital.patient',  
#     'read',  
#     [[patient_id]]  
# )
# print(patient_data)


#update operation
update_date = {
     'patient_name': 'Jane Doe'
}
patient_update = models.execute_kw(db,uid,password,"hospital.patient","write",[[patient_id],update_date])
print(patient_update)


#Delete operation
models.execute_kw(db, uid, password, 'hospital.patient', 'unlink', [[patient_id]])
print(f"Deleted Patient {patient_id}.")



# search operation
# patient_ids = models.execute_kw(db, uid, password, "hospital.patient", "search", [[]])
# print(patient_ids)





