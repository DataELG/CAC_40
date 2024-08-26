from fetch_functions import *
from date_functions import *
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, select, delete, update
from sqlalchemy.orm import sessionmaker
from datetime import date


def create_session(table_name) :
    '''
    Create a SQLAlchemy session, table object, and engine for a given table name.

    Arguments
    ----------
    table_name : str 
        The name of the table to load from the database.

    Returns
    ----------
    session : SQLAlchemy session object
        The session object used for making transactions in the database.
    table : SQLAlchemy table object
        The table object that represents the table in the database.
    engine : SQLAlchemy engine object
        The engine object that maintains the connection to the database.
    '''
    
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


def get_id(companies_table, boursorama_id, companie_session) :
    '''
    Fetch the internal ID of a company based on its Boursorama company ID.

    Arguments
    ----------
    companies_table : SQLAlchemy Table object
        The table object representing the companies in the database.
    boursorama_id : str or int
        The Boursorama company ID used to identify the company.
    companie_session : SQLAlchemy session object
        The session object used to execute the query in the database.

    Returns
    ----------
    result : int or None
        The internal ID of the company if found, or None if the company does not exist.
    '''
    stmt = select(companies_table.c.ID).where(companies_table.c.BOURSORAMA_CIE_ID == boursorama_id)
    result = companie_session.execute(stmt).scalar_one_or_none()
    return result
    

def insert_company(companies_table, companie_name, boursorama_cie_id, entry_date, session):
    '''
    Insert a new company into the companies table.

    Arguments
    ----------
    companies_table : SQLAlchemy Table object
        The table object representing the companies in the database.
    companie_name : str
        The name of the company to be inserted.
    boursorama_cie_id : str or int
        The Boursorama company ID for the new company.
    entry_date : date or datetime
        The date the company was added to the CAC40 index or database.
    session : SQLAlchemy session object
        The session object used to execute the insert operation and commit the changes.

    Returns
    ----------
    None
        The function does not return any value.
    '''

    insert_stmt = companies_table.insert().values(
        COMPANIE_NAME=companie_name,
        BOURSORAMA_CIE_ID=boursorama_cie_id,
        ENTRY_DATE=entry_date
    )
    session.execute(insert_stmt)
    session.commit()
        

def insert_history(history_table, session, companie_id,data):
    '''
    Insert historical data into the history table for a specific company.

    Arguments
    ----------
    history_table : SQLAlchemy Table object
        The table object representing the history records in the database.
    session : SQLAlchemy session object
        The session object used to execute the insert operations and commit the changes.
    companie_id : int
        The internal ID of the company for which the history is being recorded.
    data : dict or list of dicts
        The historical data to be inserted. If `data` is a list, each element should be a dictionary 
        containing 'Day', 'Opening', 'Highest', 'Lowest', 'Closing', and 'Volume' keys. 
        If `data` is a single dictionary, it should contain the same keys for a single day's data.

    Returns
    ----------
    None
        The function does not return any value.
    '''

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
    '''
    Insert a single streaming data record into the streaming table for a specific company.

    Arguments
    ----------
    streaming_table : SQLAlchemy Table object
        The table object representing the streaming data records in the database.
    session : SQLAlchemy session object
        The session object used to execute the insert operation and commit the changes.
    companie_id : int
        The internal ID of the company for which the streaming data is being recorded.
    data : dict
        A dictionary containing the streaming data with keys: 'Day', 'Opening', 'Highest', 
        'Lowest', 'Closing', and 'Volume'.

    Returns
    ----------
    None
        The function does not return any value.
    '''
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
            
            
def delete_data(nbre_jours, session, table) :
    '''
    Delete data older than a specified number of days.

    Arguments
    ----------
    nbre_jours : int
        The number of days to keep streaming data. Records older than this will be deleted.
    session : SQLAlchemy session object
        The session object used to execute the delete operation and commit the changes.
    table : SQLAlchemy Table object
        The table object representing the streaming data records in the database.

    Returns
    ----------
    None
        The function does not return any value.
    '''
    date = datetime.now() - timedelta(days=nbre_jours)
    delete_stmt = delete(table).where(table.c.DATE < date)
    session.execute(delete_stmt)
    session.commit()
    
    
def update_exit_date(session, companies_table,missing_element) :
    '''
    Update the exit date of a company in the companies table.

    Arguments
    ----------
    session : SQLAlchemy session object
        The session object used to execute the update operation and commit the changes.
    companies_table : SQLAlchemy Table object
        The table object representing the companies in the database.
    missing_element : str or int
        The Boursorama company ID of the company whose exit date is to be updated.

    Returns
    ----------
    None
        The function does not return any value.
    '''
    stmt = update(companies_table).where(companies_table.c.BOURSORAMA_CIE_ID == missing_element).values(EXIT_DATE=date.today())
    session.execute(stmt)
    session.commit()
