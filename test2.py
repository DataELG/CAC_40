import pandas as pd
from sqlalchemy import create_engine

def create_session(table_name) :
    connection_url = (
    "mssql+pyodbc://elg_admin:9w4kQ&2eUcmMqdSftT@cac40server.database.windows.net:1433/BDD_CAC40?"
    "driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
    )
    engine = create_engine(connection_url) 

    return engine

engine = create_session('STREAMING')

# Requête SQL avec jointure pour récupérer les noms des entreprises
query = """
SELECT 
    S.*, 
    C.COMPANIE_NAME 
FROM 
    [dbo].[STREAMING] S
INNER JOIN 
    [dbo].[COMPANIES] C ON S.COMPANIE_ID = C.ID
"""

# Charger les données depuis la base de données dans un DataFrame
df = pd.read_sql(query, engine)

# Convertir la colonne DATE en format datetime
df['DATE'] = pd.to_datetime(df['DATE'])

# Extraire la date la plus récente (aujourd'hui) et la date précédente (hier)
max_date = df['DATE'].max()
prev_date = df[df['DATE'] < max_date]['DATE'].max()

# Filtrer les données pour aujourd'hui et hier
df_today = df[df['DATE'] == max_date].copy()
df_yesterday = df[df['DATE'] == prev_date].copy()

# Joindre les deux DataFrames sur COMPANIE_ID et COMPANIE_NAME
merged_df = pd.merge(df_today, df_yesterday, on=['COMPANIE_ID', 'COMPANIE_NAME'], suffixes=('_TODAY', '_YESTERDAY'))

# Calculer la variation en pourcentage du prix
merged_df['PERCENTAGE_VARIATION'] = ((merged_df['CLOSING_TODAY'] - merged_df['CLOSING_YESTERDAY']) / merged_df['CLOSING_YESTERDAY']) * 100

# Calculer le changement de volume
merged_df['VOLUME_CHANGE'] = merged_df['VOLUME_TODAY'] - merged_df['VOLUME_YESTERDAY']

# Sélectionner les colonnes dans l'ordre souhaité
final_df = merged_df[['COMPANIE_NAME', 'CLOSING_TODAY', 'CLOSING_YESTERDAY', 'VOLUME_TODAY', 'VOLUME_YESTERDAY', 'PERCENTAGE_VARIATION', 'VOLUME_CHANGE']]

# Fonction pour appliquer des couleurs
def color_negative_red(val):
    if val < 0:
        color = 'red'
    else:
        color = 'green'
    return f'color: {color}'

# Appliquer les styles conditionnels avec map
styled_df = final_df.style.map(color_negative_red, subset=['PERCENTAGE_VARIATION', 'VOLUME_CHANGE'])

# Afficher le DataFrame stylisé
print(final_df)
