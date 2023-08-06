from pytz import timezone
from datetime import datetime


def make_aware(date):
    return datetime(date.year, date.month, date.day, tzinfo=timezone('America/Sao_Paulo'))
