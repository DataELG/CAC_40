import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import os


def create_report(engine) :
    '''
    Generate a financial report comparing the latest company stock data with the previous day's data.
    
    Arguments
    ----------
    engine : SQLAlchemy Engine object
        The SQLAlchemy engine connected to the database from which data will be retrieved.
        
    Returns
    ----------
    html_table : str
        An HTML string representing the final styled table, which includes company names, 
        closing prices for today and yesterday, percentage variation in prices, and changes 
        in trading volume.
    '''
    
    query = """
    SELECT 
        C.COMPANIE_NAME,
        S.*
    FROM 
        [dbo].[COMPANIES_HISTORY] as S
    INNER JOIN 
        [dbo].[COMPANIES] as C ON S.COMPANIE_ID = C.ID
    """
    df = pd.read_sql(query, engine)
    df['DATE'] = pd.to_datetime(df['DATE']) # make sure 'DATE' column is datetime

    # Extract the most recent date and the date before that
    max_date = df['DATE'].max()
    prev_date = df[df['DATE'] < max_date]['DATE'].max()

    # Filter data
    df_today = df[df['DATE'] == max_date].copy()
    df_yesterday = df[df['DATE'] == prev_date].copy()

    # Joi  both DataFrames on COMPANIE_ID et COMPANIE_NAME
    merged_df = pd.merge(df_today, df_yesterday, on=['COMPANIE_ID', 'COMPANIE_NAME'], suffixes=('_TODAY', '_YESTERDAY'))

    # Calculate % variation of price
    merged_df['PERCENTAGE_VARIATION'] = ((merged_df['CLOSING_TODAY'] - merged_df['CLOSING_YESTERDAY']) / merged_df['CLOSING_YESTERDAY']) * 100

    # Calculate changing  in volume
    merged_df['VOLUME_CHANGE'] = merged_df['VOLUME_TODAY'] - merged_df['VOLUME_YESTERDAY']

    # Select columnn  in desired order
    final_df = merged_df[['COMPANIE_NAME', 'CLOSING_TODAY', 'CLOSING_YESTERDAY', 'VOLUME_TODAY', 'VOLUME_YESTERDAY', 'PERCENTAGE_VARIATION', 'VOLUME_CHANGE']]
    # Afficher le résultat final

    # Applicate color : green if postive, red if negative
    def color_negative_red(value):
        color = 'red' if value < 0 else 'green'
        return f'color: {color}'

    # Apply style to df
    styled_df = final_df.style.map(color_negative_red, subset=['PERCENTAGE_VARIATION', 'VOLUME_CHANGE'])
    html_table = styled_df.to_html()

    return html_table



def send_email(html_table) :
    '''
    Send an email with an HTML table containing the market report.
    
    Arguments
    ----------
    html_table : str
        An HTML string representing the market report table to be included in the email body.

    Returns
    ----------
    None
        The function does not return any value but prints success or error messages.
    '''
    sender = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    receiver = os.getenv('RECIPIENT')

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Rapport du Marché - Variation des Actions'

    # e-mail body
    body = f"""
    <h2>Bonjour,</h2>
    <p>Voici le rapport des variations de prix et de volumes pour aujourd'hui :</p>
    {html_table}
    <p>Cordialement,<br>DataTradeX</p>
    """

    # Attached e-mail body
    msg.attach(MIMEText(body, 'html'))

    # Connenxion to server
    try:
        server = smtplib.SMTP('smtp.office365.com', 587) 
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
        