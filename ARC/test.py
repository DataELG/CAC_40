import requests
from datetime import datetime, timedelta, date
from utils.fetch_functions import *
import pandas as pd
from IPython.display import display


# boursorama_cie_ID = ''
# url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPSU&length=1&period=0&guid='
# response = requests.get(url)
# if response.status_code == 200:
#     response_json = response.json()
#     data = response_json['d']['QuoteTab']

    
# def get_date(date) :
#     date_reference = datetime(1970, 1, 1)
#     day_clean = date_reference + timedelta(days=date)
#     #day_formatee = day_clean.strftime("%Y-%m-%d")
#     return day_clean

# print(get_date(19948))

# from datetime import datetime, timedelta

# def decode_datetime(date_str):
#     # Extraction des parties de la chaîne
#     year = int("20" + date_str[:2])  # "24" -> 2024
#     month = int(date_str[2:4])       # "08" -> Août
#     day = int(date_str[4:6])         # "13" -> 13
#     time_in_minutes = int(date_str[6:10])  # "1057" -> 1057 minutes depuis minuit

#     # Calcul de l'heure et des minutes à partir des minutes écoulées depuis minuit
#     hours = time_in_minutes // 60   # Calcul du nombre d'heures
#     minutes = time_in_minutes % 60  # Calcul des minutes restantes

#     return datetime(year, month, day, hours, minutes) 

# # Exemple d'utilisation
# date_str = "2408131057"
# decoded_date = decode_datetime(date_str)
# print(decoded_date)
today = date.today()
yesterday = today - timedelta(days = 1)
session_companies_table, companies_table,engine = create_session('COMPANIES')

# 1 - get  id toutes les cies


# list_cac40_cie = fetch_active_CAC40_cie(companies_table,session_companies_table)
# print(list_cac40_cie)
# 2 - get données clotures today

# 3 - get données clotures yesterday 
# tableau 


def create_session(table_name) :
    connection_url = (
    "mssql+pyodbc://elg_admin:9w4kQ&2eUcmMqdSftT@cac40server.database.windows.net:1433/BDD_CAC40?"
    "driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
    )
    engine = create_engine(connection_url) 

    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session, table, engine

session, table, engine = create_session('STREAMING')

# query_closing_today = """
# SELECT 
#     A.COMPANIE_ID, 
#     B.COMPANIE_NAME, 
#     A.DATE as CLOSING_TIME, 
#     A.CLOSING,
#     A.VOLUME
# FROM 
#     [dbo].[STREAMING] as A
# INNER JOIN 
#     [dbo].[COMPANIES] as B ON A.COMPANIE_ID = B.ID
# WHERE 
#     A.DATE = (
#         SELECT MAX(A2.DATE) 
#         FROM [dbo].[STREAMING] as A2 
#         WHERE A2.COMPANIE_ID = A.COMPANIE_ID
#     )
# ORDER BY 
#     A.COMPANIE_ID;
# """
# df_closing_today = pd.read_sql(query_closing_today, con=engine)
# print(df_closing_today.head())
# print(len(df_closing_today))

# query_closing_yesterday = """
# SELECT 
#     A.COMPANIE_ID, 
#     B.COMPANIE_NAME, 
#     A.DATE as CLOSING_TIME, 
#     A.CLOSING,
#     A.VOLUME
# FROM 
#     [dbo].[COMPANIES_HISTORY] as A
# INNER JOIN 
#     [dbo].[COMPANIES] as B ON A.COMPANIE_ID = B.ID
# WHERE 
#     A.DATE = (
#         SELECT MAX(A2.DATE) 
#         FROM [dbo].[COMPANIES_HISTORY] as A2 
#         WHERE A2.COMPANIE_ID = A.COMPANIE_ID
#     )
# ORDER BY 
#     A.COMPANIE_ID;
# """
# df_closing_yesterday = pd.read_sql(query_closing_yesterday, con=engine)
# print(df_closing_yesterday.head())
# print(len(df_closing_yesterday))


# # # Joindre les deux DataFrames sur COMPANIE_ID et COMPANIE_NAME
# # merged_df = pd.merge(df_closing_today, query_closing_yesterday, on=['COMPANIE_ID', 'COMPANIE_NAME'], suffixes=('_TODAY', '_YESTERDAY'))

# # # Calculer la variation en pourcentage
# # merged_df['PERCENTAGE_VARIATION'] = ((merged_df['CLOSING_TODAY'] - merged_df['CLOSING_YESTERDAY']) / merged_df['CLOSING_YESTERDAY']) * 100

# #  #Trier par variation en pourcentage dans l'ordre décroissant
# # sorted_df = merged_df.sort_values(by='PERCENTAGE_VARIATION', ascending=False)

# # # Afficher le DataFrame trié
# # print(sorted_df[['COMPANIE_ID', 'COMPANIE_NAME', 'CLOSING_TIME_TODAY', 'CLOSING_TODAY', 'CLOSING_TIME_YESTERDAY', 'CLOSING_YESTERDAY', 'PERCENTAGE_VARIATION']])
# # # Fermer la session
# # Joindre les deux DataFrames sur COMPANIE_ID et COMPANIE_NAME
# merged_df = pd.merge(df_closing_today, df_closing_yesterday, on=['COMPANIE_ID', 'COMPANIE_NAME'], suffixes=('_TODAY', '_YESTERDAY'))

# # Calculer la variation en pourcentage du prix
# merged_df['PERCENTAGE_VARIATION'] = ((merged_df['CLOSING_TODAY'] - merged_df['CLOSING_YESTERDAY']) / merged_df['CLOSING_YESTERDAY']) * 100

# # Calculer le changement de volume
# merged_df['VOLUME_CHANGE'] = merged_df['VOLUME_TODAY'] - merged_df['VOLUME_YESTERDAY']

# # Trier par les plus grandes variations de prix, puis par volume décroissant
# sorted_df = merged_df.sort_values(by=['PERCENTAGE_VARIATION', 'VOLUME_TODAY'], ascending=[False, False])

# # Afficher les résultats pertinents
# print(sorted_df[['COMPANIE_ID', 'COMPANIE_NAME', 'CLOSING_TIME_TODAY', 'CLOSING_TODAY', 'VOLUME_TODAY', 'PERCENTAGE_VARIATION', 'VOLUME_CHANGE']])


