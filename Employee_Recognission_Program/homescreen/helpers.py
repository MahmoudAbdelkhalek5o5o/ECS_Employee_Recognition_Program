from datetime import datetime

def check_date(start_date):
    if datetime.now() >= start_date:
        return True
    else:
        return False
    

    