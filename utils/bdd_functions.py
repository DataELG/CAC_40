from utils.fetch_functions import *
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, select, delete, update
from sqlalchemy.orm import sessionmaker
from datetime import date

today = date.today()    


def get_date(date) :
    date_reference = datetime(1970, 1, 1)
    day_clean = date_reference + timedelta(days=date)
    #day_formatee = day_clean.strftime("%Y-%m-%d")
    return day_clean


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


def fetch_active_CAC40_cie(companies_table, session) :
    '''
    Return a list of companies added today
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID).where(companies_table.c.EXIT_DATE.is_(None))
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list


def fetch_all_CAC40_cie(companies_table, session) :
    '''
    Return a list of CAC cie (activve one and ancient one
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID)
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list


def get_id(companies_table, boursorama_id, companie_session) :
    '''
    Return the ID of the companie
    '''
    stmt = select(companies_table.c.ID).where(companies_table.c.BOURSORAMA_CIE_ID == boursorama_id)
    result = companie_session.execute(stmt).scalar_one_or_none()
    return result
    

def insert_company(companies_table, companie_name, boursorama_cie_id, entry_date, session):

    insert_stmt = companies_table.insert().values(
        COMPANIE_NAME=companie_name,
        BOURSORAMA_CIE_ID=boursorama_cie_id,
        ENTRY_DATE=entry_date
    )
    session.execute(insert_stmt)
    session.commit()
        

def insert_history(history_table, session, companie_id,data):

    if isinstance(data,list) :
        for i in range(len(data['Day'])) :
            insert_stmt = history_table.insert().values(
                COMPANIE_ID=companie_id,
                DATE=data['Day'][i],
                OPENING=data['Opening'][i],
                HIGHEST=data['Highest'][i],
                LOWEST=data['Lowest'][i],
                CLOSING=data['Closing'][i],
                VOLUME=data['Volume'][i]
            )
            session.execute(insert_stmt)
            session.commit()
            
    else : 
        insert_stmt = history_table.insert().values(
                COMPANIE_ID=companie_id,
                DATE=data['Day'],
                OPENING=data['Opening'],
                HIGHEST=data['Highest'],
                LOWEST=data['Lowest'],
                CLOSING=data['Closing'],
                VOLUME=data['Volume']
            )
        session.execute(insert_stmt)
        session.commit()
        
            
def insert_streaming(streaming_table, session, companie_id,data):

    insert_stmt = streaming_table.insert().values(
        COMPANIE_ID=companie_id,
        DATE=data['Day'],
        OPENING=data['Opening'],
        HIGHEST=data['Highest'],
        LOWEST=data['Lowest'],
        CLOSING=data['Closing'],
        VOLUME=data['Volume']
    )
    session.execute(insert_stmt)
    session.commit()            
            
            
def delete_streaming_data(nbre_jours, session, streaming_table) :
    date = datetime.now() - timedelta(days=nbre_jours)
    delete_stmt = delete(streaming_table).where(streaming_table.c.DATE < date)
    session.execute(delete_stmt)
    session.commit()
    
    
def update_exit_date(session, companies_table,missing_element) :
    stmt = update(companies_table).where(companies_table.c.BOURSORAMA_CIE_ID == missing_element).values(EXIT_DATE=today)
    session.execute(stmt)
    session.commit()


