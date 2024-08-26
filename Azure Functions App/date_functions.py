from datetime import datetime,timedelta


def get_date(date) :
    '''
    Arguments
    ----------
    date : int 
        corresponding number of day since January 1st, 1970
        
    Returns
    ----------  
    datetime 

    '''
    date_reference = datetime(1970, 1, 1)
    day_clean = date_reference + timedelta(days=date)
    day_formatee = day_clean.strftime("%Y-%m-%d")
    return day_formatee


def decode_datetime(date_str):
    '''
    Transform date this format YYmmddMMMM to datetime. 
    ex : 2408150543
    24 : year
    08 : month
    13 : day
    1057 : minutes since midnight
    
    Arguments
    ----------
    date : str 
        
    Returns
    ----------  
    datetime 
    
    '''
    year = int("20" + date_str[:2])  
    month = int(date_str[2:4])       
    day = int(date_str[4:6])         
    time_in_minutes = int(date_str[6:10])  

    # Calculate the hour and minutes from the number of minutes elapsed since midnight
    hours = time_in_minutes // 60   # Calculate the number of hours
    minutes = time_in_minutes % 60  # Calculate the remaining minutes

    return datetime(year, month, day, hours, minutes) 
    