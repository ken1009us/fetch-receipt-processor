from datetime import datetime


def validate_date(date_str):
    """
    Validates the date string in the format "YYYY-MM-DD".
    Returns True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """
    Validates the time string in the format "HH:MM".
    Returns True if the time is valid, False otherwise.
    """
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_receipt_data(receipt_data):
    """
    Validates the receipt data dictionary.
    Returns True if the data is valid, False otherwise.
    """
    retailer = receipt_data.get('retailer')
    purchase_date = receipt_data.get('purchaseDate')
    purchase_time = receipt_data.get('purchaseTime')
    total = receipt_data.get('total')
    items = receipt_data.get('items')

    if not retailer or not purchase_date or not purchase_time or not total or not items:
        return False

    if not validate_date(purchase_date) or not validate_time(purchase_time):
        return False

    for item in items:
        if not item.get('shortDescription') or not item.get('price'):
            return False

    return True
