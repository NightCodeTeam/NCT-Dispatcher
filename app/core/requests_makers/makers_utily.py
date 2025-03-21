from datetime import datetime


def time_to_json(time: datetime):
    return time.strftime('%H:%M:%S %d-%m-%Y')

def time_from_json(time):
    return datetime.strptime(time, '%H:%M:%S %d-%m-%Y')

def headers_to_json(headers):
    return dict(headers)
