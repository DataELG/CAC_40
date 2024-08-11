from utils.fetch_data import *
from utils.bdd_functions import *
from utils.req_functions import *
from datetime import date
import pandas as pd

today = date.today()

# 0.0 - Add data history veille

# 0 - Delete stream + 90 jours


# 1 - Get companies name and ID -- OK
companies_dict = fetch_companies_info()     
session_companie_table, companies_table = create_session('COMPANIES') 

for key, value in companies_dict.items():
    insert_company(companies_table, key, value, today, session_companie_table)


# 2 - Get history of new companies
new_companies_id = fetch_new_companies(companies_table, session_companie_table)
for id in new_companies_id :
    companie_history = fetch_history(id)
    insert_history(companie_history)

session_companie_table.close() 
    
# 3 - Get data every 2 mins




# 4 - Send e-mail end of day