from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

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