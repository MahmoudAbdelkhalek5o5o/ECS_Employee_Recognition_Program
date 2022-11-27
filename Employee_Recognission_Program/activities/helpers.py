from datetime import datetime
import pytz

def check_date(start_date):
    utc=pytz.UTC

    if utc.localize(datetime.now()) >= start_date:
        return True
    else:
        return False
    
