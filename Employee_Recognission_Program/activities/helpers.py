import datetime
import pytz

def check_date(start_date):

    if datetime.date.today() >= start_date:
        return True
    else:
        return False
    
