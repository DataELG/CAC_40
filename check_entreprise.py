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


# Delete stream + 180 jours - FONCTIONNE 14/08
# delete_streaming_data(180, session_streaming_table, streaming_table)


# Add day data of the day before to history - FONCTIONNE 14/08 (data du 13 août ajouté)
# list_cac40_cie = fetch_all_CAC40_cie(companies_table,session_companies_table)  # ajout data actual and anciennt cac40 cie
# for boursorama_cie_ID in list_cac40_cie :
#     cie_id = get_id(companies_table, boursorama_cie_ID, session_companies_table)
#     print(cie_id)
#     data = fetch_yesterday_history(boursorama_cie_ID)
#     data_date = data['Day']
#     existing_entry = session_history_table.query(history_table).filter_by(COMPANIE_ID=cie_id, DATE=data_date).first()
#     if existing_entry is None:     # Si la date n'exite pas déjà pour cet ID :
#         insert_history(history_table, session_companies_table, cie_id,data)


# Get companies name and ID -- FONCTIONNE 14/08
# actual_companies = fetch_active_CAC40_cie(companies_table,session_companies_table) # Vérifie les companies qui n'ont pas quitté le CAC40 dans notre base
# companies_dict = fetch_companies_info() # Récupère les entreprises qui sont dans le CAC40 en date du jour
# for key, value in companies_dict.items(): # Si l'entreprise n'est pas dans notre table COMPANIES, l'ajouter
#     existing_company = session_companies_table.query(companies_table).filter_by(BOURSORAMA_CIE_ID=value).first()
#     if existing_company is None:
#         insert_company(companies_table, key, value, today, session_companies_table)

    # Find the missing company and update the exit date on today's date - FONCTIONE 14/08
# today_cie = companies_dict.values()
# missing_element = list(set(actual_companies) - set(today_cie))
# if len(missing_element) > 1 :
#     update_exit_date(session_companies_table, companies_table,missing_element)


# Get history of new companies - FONCTIONNE 14/08
# new_companies_id = fetch_new_companies(companies_table, session_companies_table)
# if new_companies_id :
#     for boursorama_cie_ID in new_companies_id:
#         cie_id = get_id(companies_table, boursorama_cie_ID, session_companies_table)
#         check_presence_history = session_history_table.query(history_table).filter_by(COMPANIE_ID=cie_id).first()
#         if check_presence_history is None :  # Si l'historique de cette entreprise n'est pas déjà enregistrée
#             companie_history = fetch_history_data(boursorama_cie_ID)
#             insert_history(history_table, session_history_table,cie_id,companie_history)
        

# 3 - Get data every 15 mins -- FONCTIONNE 14/08
# list_cac40_cie = fetch_active_CAC40_cie(companies_table,session_companies_table)
# for boursorama_cie_ID in list_cac40_cie :
#     key_id = get_id(companies_table,boursorama_cie_ID,session_companies_table)
#     data = fetch_streaming_data(boursorama_cie_ID)
#     exists = session_streaming_table.query(streaming_table).filter_by(COMPANIE_ID=key_id, DATE=data['Day']).first()
#     if exists is None:
#         insert_streaming(streaming_table,session_streaming_table,key_id, data)


# 4 - Send e-mail end of day






session_history_table.close()
session_companies_table.close() 
session_streaming_table.close()