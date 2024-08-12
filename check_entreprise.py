from utils.fetch_data import *
from utils.bdd_functions import *
from utils.req_functions import *
from datetime import date
import pandas as pd

today = date.today()

# Delare sessions
session_companies_table, companies_table = create_session('COMPANIES')
session_history_table, history_table = create_session('COMPANIES_HISTORY') 
session_streaming_table, streaming_table = create_session('STREAMING')  


# Add day data of the day  before



# Delete stream + 180 jours
delete_streaming_data(180, session_streaming_table, streaming_table)

# Get companies name and ID -- OK
companies_dict = fetch_companies_info()     

for key, value in companies_dict.items():
    insert_company(companies_table, key, value, today, session_companies_table)


# Get history of new companies
new_companies_id = fetch_new_companies(companies_table, session_companies_table)
for id in new_companies_id :
    key_id = get_id(companies_table,id,session_companies_table)
    companie_history = fetch_data(id, 'history')
    insert_history(history_table, session_history_table,key_id,companie_history)
    

# 3 - Get data every 15 mins
list_cac40_cie = fetch_CAC40_cie(companies_table,session_companies_table)
for companie in list_cac40_cie :
    key_id = get_id(companies_table,id,session_companies_table)
    data = fetch_data(companie, 'streaming')
    insert_streaming(streaming_table,session_streaming_table,key_id, data)



# 4 - Send e-mail end of day





session_history_table.close()
session_companies_table.close() 