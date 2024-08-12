from utils.fetch_functions import *
from utils.bdd_functions import *
from utils.req_functions import *
from datetime import date
import pandas as pd

today = date.today()

# Delare sessions
session_companies_table, companies_table = create_session('COMPANIES')
session_history_table, history_table = create_session('COMPANIES_HISTORY') 
session_streaming_table, streaming_table = create_session('STREAMING')  


# Delete stream + 180 jours - OK
delete_streaming_data(180, session_streaming_table, streaming_table)

# Add day data of the day before to history

"qv"

# Get companies name and ID -- OK
actual_companies = fetch_CAC40_cie(companies_table,session_companies_table)
companies_dict = fetch_companies_info() 
for key, value in companies_dict.items():
    insert_company(companies_table, key, value, today, session_companies_table)

    # Find the missing company and update the exit date on today's date - OK
today_cie = companies_dict.values()
missing_element = list(set(actual_companies) - set(today_cie))
if len(missing_element) > 1 :
    update_exit_date(session_companies_table, companies_table,missing_element)


# Get history of new companies - OK
# new_companies_id = fetch_new_companies(companies_table, session_companies_table)
# for boursorama_id in new_companies_id:
#     key_id = get_id(companies_table,boursorama_id,session_companies_table) # OK
#     companie_history = fetch_data(boursorama_id, 'history')
#     insert_history(history_table, session_history_table,key_id,companie_history)
    

# 3 - Get data every 15 mins
list_cac40_cie = fetch_CAC40_cie(companies_table,session_companies_table)
for companie_id in list_cac40_cie :
    key_id = get_id(companies_table,companie_id,session_companies_table)
    data = fetch_data(companie_id, 'streaming')
    # insert_streaming(streaming_table,session_streaming_table,key_id, data)

# 4 - Send e-mail end of day





session_history_table.close()
session_companies_table.close() 