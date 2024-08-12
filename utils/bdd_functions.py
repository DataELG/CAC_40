from fetch_data import *
from sqlalchemy import create_engine, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker
from datetime import date

today = date.today()

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
    return session, table


def fetch_new_companies(companies_table, session) :
    '''
    Return a list of companies added today
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID).where(companies_table.c.ENTRY_DATE == today)
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list


def fetch_CAC40_cie(companies_table, session) :
    '''
    Return a list of companies added today
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID).where(companies_table.c.EXIT_DATE.is_(None))
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list



def get_id(companies_table, boursorama_id, companie_session) :
    '''
    Return the ID of the companie
    '''
    stmt = select(companies_table.c.ID).where(companies_table.c.BOURSORAMA_CIE_ID == boursorama_id)
    companie_session.execute(stmt)
    companie_session.commit()
    

def insert_company(companies_table, companie_name, boursorama_cie_id, entry_date, session):
    # Vérifier si la valeur BOURSORAMA_CIE_ID existe déjà
    existing_company = session.query(companies_table).filter_by(BOURSORAMA_CIE_ID=boursorama_cie_id).first()
    
    if existing_company is None:
        # Préparer l'insertion
        insert_stmt = companies_table.insert().values(
            COMPANIE_NAME=companie_name,
            BOURSORAMA_CIE_ID=boursorama_cie_id,
            ENTRY_DATE=entry_date
        )
        session.execute(insert_stmt)
        session.commit()
        

def insert_history(history_table, session, companie_id,data):
    existing_company = session.query(history_table).filter_by(COMPANIE_ID=companie_id).first()
    
    if existing_company is None:
        # Préparer l'insertion
        for i in range(len(data)) :
            day = data['Day'][i]
            date_hist = get_date(day)
            insert_stmt = history_table.insert().values(
                COMPANIE_ID=companie_id,
                DATE=date_hist,
                OPENING=data['Opening'][i],
                HIGHEST=data['Highest'][i],
                LOWEST=data['Lowest'][i],
                CLOSING=data['Closing'][i],
                VOLUME=data['Volume'][i]
            )
            session.execute(insert_stmt)
            session.commit()
            
            
def insert_streaming(streaming_table, session, companie_id,data):
    existing_company = session.query(streaming_table).filter_by(COMPANIE_ID=companie_id).first()
    
    if existing_company is None:
        # Préparer l'insertion
        for i in range(len(data)) :
            day = data['Day'][i]
            date_hist = get_date(day)
            insert_stmt = streaming_table.insert().values(
                COMPANIE_ID=companie_id,
                DATE=date_hist,
                OPENING=data['Opening'][i],
                HIGHEST=data['Highest'][i],
                LOWEST=data['Lowest'][i],
                CLOSING=data['Closing'][i],
                VOLUME=data['Volume'][i]
            )
            session.execute(insert_stmt)
            session.commit()            
            
            
def delete_streaming_data(nbre_jours, session, streaming_table) :
    delete_stmt = delete(streaming_table).where(streaming_table.c.DATE < nbre_jours)
    session.execute(delete_stmt)
    session.commit()