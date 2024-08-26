import logging
import azure.functions as func
from fetch_functions import *
from bdd_functions import *
from req_functions import *
from email_functions import *
from date_functions import *
from datetime import date


app = func.FunctionApp()

@app.timer_trigger(schedule="0 50 8 * * 1-5", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def check_new_company(myTimer: func.TimerRequest) -> None:

    # Delare sessions
    session_companies_table, companies_table, engine = create_session('COMPANIES')
    session_history_table, history_table, engine = create_session('COMPANIES_HISTORY') 

    # Get companies name and ID
    actual_companies = fetch_active_CAC40_cie(companies_table,session_companies_table) # Check companie with no exit date
    companies_dict = fetch_companies_info() # Get cie on CAC40 today
    for key, value in companies_dict.items(): # check for new company added
        existing_company = session_companies_table.query(companies_table).filter_by(BOURSORAMA_CIE_ID=value).first()
        if existing_company is None:
            logging.info('A new companie has joined CAC40!')
            insert_company(companies_table, key, value, date.today(), session_companies_table)

    # Find the missing company and update the exit date on today's date - FONCTIONE 14/08
    today_cie = companies_dict.values()
    missing_element = list(set(actual_companies) - set(today_cie))
    if len(missing_element) > 1 :
        logging.info('A companie has left CAC40!')
        update_exit_date(session_companies_table, companies_table,missing_element)
    else : 
        logging.info('No companie has left CAC40 today !')


    # Get history of new companies
    new_companies_id = fetch_new_companies(companies_table, session_companies_table)
    if new_companies_id :
        for boursorama_cie_ID in new_companies_id:
            cie_id = get_id(companies_table, boursorama_cie_ID, session_companies_table)
            check_presence_history = session_history_table.query(history_table).filter_by(COMPANIE_ID=cie_id).first()
            if check_presence_history is None :  # If history  not in our base, get it
                logging.info('History of the new company added!')
                companie_history = fetch_history_data(boursorama_cie_ID)
                insert_history(history_table, session_history_table,cie_id,companie_history)

    session_history_table.close()
    session_companies_table.close() 
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')


@app.timer_trigger(schedule="0 */10 9-18 * * 1-5", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def get_trading_data(myTimer: func.TimerRequest) -> None:
    # Delare sessions
    session_companies_table, companies_table, engine = create_session('COMPANIES')
    session_streaming_table, streaming_table, engine = create_session('STREAMING')
    
    # 3 - Get data every 10 mins 
    list_cac40_cie = fetch_active_CAC40_cie(companies_table,session_companies_table)
    for boursorama_cie_ID in list_cac40_cie :
        key_id = get_id(companies_table,boursorama_cie_ID,session_companies_table)
        data = fetch_streaming_data(boursorama_cie_ID)
        exists = session_streaming_table.query(streaming_table).filter_by(COMPANIE_ID=key_id, DATE=data['Day']).first()
        if exists is None:
            insert_streaming(streaming_table,session_streaming_table,key_id, data)
    
    session_companies_table.close() 
    session_streaming_table.close()
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

@app.timer_trigger(schedule="0 50 17 * * 1-5", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def cleaning_end_day(myTimer: func.TimerRequest) -> None:

    # Create session
    session_companies_table, companies_table, engine = create_session('COMPANIES')
    session_history_table, history_table, engine = create_session('COMPANIES_HISTORY') 
    session_streaming_table, streaming_table, engine = create_session('STREAMING') 
    logging.info('SESSION OPENED') 

    # Add day data of TODAY END OF DAY
    list_cac40_cie = fetch_all_CAC40_cie(companies_table,session_companies_table)  # get actual and ancient cie code 
    for boursorama_cie_ID in list_cac40_cie :
        cie_id = get_id(companies_table, boursorama_cie_ID, session_companies_table)
        data = fetch_today_history(boursorama_cie_ID)
        data_date = data['Day']
        existing_entry = session_history_table.query(history_table).filter_by(COMPANIE_ID=cie_id, DATE=data_date).first()
        if existing_entry is None:     # Si la date n'exite pas déjà pour cet ID :
            logging.info(f'History of today added for {boursorama_cie_ID}')
            insert_history(history_table, session_history_table, cie_id,data)
    
    # Send recap e-mail
    html_table = create_report(engine)
    send_email(html_table)
    
    # Delete stream + 180 days
    delete_data(180, session_streaming_table, streaming_table)

    # Delete history data + 3 years
    delete_data(1094, session_history_table, history_table)

    # Close session
    session_history_table.close()
    session_companies_table.close() 
    session_streaming_table.close()
    

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')