
from datetime import datetime
from utils.requestAPI import *
from utils.fetch_data import *
from utils.SQL_functions import *

# Get companies name and ID
companies_dict = fetch_companies_info()     
session, companies_table = create_session('COMPANIES') 

for key, value in companies_dict.items():
    insert_company(companies_table, key, value, datetime.now(), session)
session.close() 