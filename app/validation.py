from datetime import datetime


def validate_date(date_str):
    """
    Validates the date string in the format "YYYY-MM-DD".
    Returns True if the date is valid, False otherwise.
    """
    try:
        date_str = datetime.strptime(date_str, "%Y-%m-%d")
        year, month, day = map(int, date_str.split('-'))
        if year > 9999 or year < 1:
            return False
        if month > 12 or month < 1:
            return False
        if day > 31 or day < 1:
            return False
        return True
    except ValueError:
        return False


def validate_time(time_str):
    """
    Validates the time string in the format "HH:MM".
    Returns True if the time is valid, False otherwise.
    """
    try:
        time_str = datetime.strptime(time_str, "%H:%M")
        hour, minute = map(int, time_str.split(':'))
        if hour > 23 or hour < 1:
            return False
        if minute > 59 or minute < 1:
            return False
        return True
    except ValueError:
        return False

def validate_receipt_data(receipt_data):
    """
    Validates the receipt data dictionary.
    Returns True if the data is valid, False otherwise.
    """
    retailer = receipt_data.get('retailer')
    total = receipt_data.get('total')
    items = receipt_data.get('items')

    if not retailer or not total or not items:
        return False

    for item in items:
        if not item.get('shortDescription') or not item.get('price'):
            return False

    return True
