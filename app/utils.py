"""
This module contains utility functions for generating receipt IDs, decoding receipt IDs, calculating points, and performing time conversions.

Dependencies:
- math: Provides mathematical functions.
- struct: Provides functions for working with binary data.
- uuid: Generates and manipulates UUIDs.
- datetime: Provides classes for manipulating dates and times.
- models: Contains the Item and Receipt models used in the calculations.

Functions:
- generate_receipt_id(receipt): Generates a receipt ID for a given receipt and returns it.
- decode_receipt_id(id, dict): Decodes a receipt ID using a dictionary and returns the corresponding receipt object.
- convert_time(time): Converts a time string to a formatted time string.
- calculate_points(id, uuid_dict): Calculates the points and breakdown for a given receipt ID using a dictionary of receipts.

Note: The calculate_points function assumes the presence of a decode_receipt_id function that decodes the receipt ID. The print statement in the else block of the calculate_points function suggests a possible error handling approach, but it should be adjusted based on the desired behavior.

"""


import math
import uuid

from datetime import datetime


def generate_receipt_id(receipt):
    """
    Generates a receipt ID for a given receipt and returns it.

    Parameters:
    - receipt (Receipt): The receipt object for which to generate the ID.

    Returns:
    - str: The generated receipt ID.
    """
    uuid_value = str(uuid.uuid4())
    uuid_dict = {uuid_value: receipt}

    return uuid_value


def decode_receipt_id(id, dict):
    """
    Decodes a receipt ID using a dictionary and returns the corresponding receipt object.

    Parameters:
    - id (str): The receipt ID to decode.
    - dict (dict): The dictionary containing receipt IDs and their corresponding Receipt objects.

    Returns:
    - Receipt or None: The decoded receipt object if the ID exists in the dictionary, or None otherwise.
    """
    if id in dict:
        return dict[id]
    else:
        return None


def convert_time(time):
    """
    Converts a time string to a formatted time string.

    Parameters:
    - time (str): The time string to convert.

    Returns:
    - str: The formatted time string.
    """
    time_obj = datetime.strptime(time, "%H:%M")
    formatted_time = time_obj.strftime("%-I:%M%p")
    return formatted_time


def calculate_points(id, uuid_dict):
    """
    Calculates the points and breakdown for a given receipt ID using a dictionary of receipts.

    Parameters:
    - id (str): The receipt ID for which to calculate the points.
    - uuid_dict (dict): The dictionary containing receipt IDs and their corresponding Receipt objects.

    Returns:
    - tuple: A tuple containing the calculated points (int) and breakdown (list of str).
    """
    points = 0
    breakdown = []
    receipt = decode_receipt_id(id, uuid_dict)

    if receipt:
        retailer_name = receipt.retailer
        purchase_date = receipt.purchaseDate
        purchase_time = receipt.purchaseTime
        total = float(receipt.total)
        items = receipt.items

        alphanumeric_count = 0
        alphanumeric_count += sum(char.isalnum() for char in retailer_name)
        points += alphanumeric_count
        breakdown.append(f"{alphanumeric_count} points - retailer name "
                    f"({retailer_name}) has {alphanumeric_count} alphanumeric characters")

        if total.is_integer():
            points += 50
            breakdown.append("50 points - total is a round dollar amount")

        if total % 0.25 == 0:
            points += 25
            breakdown.append("25 points - total is a multiple of 0.25")

        item_count = len(items)
        points += ((item_count // 2) * 5)
        breakdown.append(f"{((item_count // 2) * 5)} points - {item_count} items "
                    f"({item_count // 2} pairs @ 5 points each)")

        for item in items:
            description = item.shortDescription
            price = float(item.price)
            trimmed_length = len(description.strip())

            if trimmed_length % 3 == 0:
                item_points = int(math.ceil((price * 0.2)))
                points += item_points
                breakdown.append(f'{item_points} points - "{description.strip()}" is {trimmed_length} characters (a multiple of 3)'
                           f"item price of {price} * 0.2 = {round(price * 0.2, 4)}, rounded up is {item_points} points")

        _, _, purchase_day = map(int, purchase_date.split('-'))
        if (purchase_day % 2) != 0:
            points += 6
            breakdown.append("6 points - purchase day is odd")

        purchase_hour, _ = map(int, purchase_time.split(':'))
        if 14 < purchase_hour < 16:
            points += 10
            time = convert_time(purchase_time)
            breakdown.append("10 points - {time} is between 2:00pm and 4:00pm")

    else:
        print("No receipt!!")

    return points, breakdown







