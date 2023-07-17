"""
This module contains utility functions for generating receipt IDs, decoding
receipt IDs, calculating points, and performing time conversions.

Dependencies:
- math: Provides mathematical functions.
- uuid: Generates and manipulates UUIDs.
- datetime: Provides classes for manipulating dates and times.

Functions:
- generate_receipt_id(): Generates a receipt ID and returns it.
- decode_receipt_id(id, dict): Decodes a receipt ID using a dictionary and
  returns the corresponding receipt object.
- convert_time(time): Converts a time string to a formatted time string.
- calculate_points(id, uuid_dict): Calculates the points and breakdown for
  a given receipt ID using a dictionary of receipts.

"""


import math
import uuid

from datetime import datetime


def generate_receipt_id():
    """
    Generates a receipt ID and returns it.

    Returns:
    - str: The generated receipt ID.
    """
    return str(uuid.uuid4())


def decode_receipt_id(receipt_id, receipt_dict):
    """
    Decodes a receipt ID using a dictionary and returns the corresponding
    receipt object.

    Parameters:
    - receipt_id (str): The receipt ID to decode.
    - receipt_dict (dict): The dictionary containing receipt IDs and their
      corresponding Receipt objects.

    Returns:
    - Receipt or None: The decoded receipt object if the ID exists
      in the dictionary, or None otherwise.
    """
    try:
        return receipt_dict[receipt_id][0]
    except KeyError:
        return None


def convert_time(time_str):
    """
    Converts a time string to a formatted time string.

    Parameters:
    - time_str (str): The time string to convert.

    Returns:
    - str: The formatted time string.
    """
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        formatted_time = time_obj.strftime("%-I:%M%p")
        return formatted_time
    except ValueError:
        return "Invalid time format"


def calculate_points(id, uuid_dict):
    """
    Calculates the points and breakdown for a given receipt ID using
    a dictionary of receipts.

    Parameters:
    - id (str): The receipt ID for which to calculate the points.
    - uuid_dict (dict): The dictionary containing receipt IDs and
      their corresponding Receipt objects.

    Returns:
    - tuple: A tuple containing the calculated points (int)
      and breakdown (list of str).
    """
    points = 0
    breakdown = []

    try:
        receipt = decode_receipt_id(id, uuid_dict)

        if receipt:
            retailer_name = receipt.retailer
            purchase_date = receipt.purchaseDate
            purchase_time = receipt.purchaseTime
            total = float(receipt.total)
            items = receipt.items

            # Rule 1: 1 point for every alphanumeric character in retailer name
            alphanumeric_count = sum(char.isalnum() for char in retailer_name)
            points += alphanumeric_count
            if alphanumeric_count > 0:
                breakdown.append(f"{alphanumeric_count} points - retailer name has {alphanumeric_count} characters")

            # Rule 2: 50 points if total is a round dollar amount with no cents
            if total.is_integer():
                points += 50
                breakdown.append("50 points - total is a round dollar amount")

            # Rule 3: 25 points if the total is a multiple of 0.25
            if total % 0.25 == 0:
                points += 25
                breakdown.append("25 points - total is a multiple of 0.25")

            # Rule 4: 5 points for every two items on the receipt
            item_count = len(items)
            points += ((item_count // 2) * 5)
            if item_count > 1:
                if item_count % 2 == 0:
                    counted_items = item_count
                else:
                    counted_items = item_count - 1
                breakdown.append(f"{((item_count // 2) * 5)} points - {counted_items} items ({item_count // 2} pairs @ 5 points each)")

            # Rule 5: If the trimmed length of
            # the item description is a multiple of 3,
            # multiply the price by 0.2 and round up to the nearest integer.
            # The result is the number of points earned
            for item in items:
                description = item.shortDescription
                price = float(item.price)
                trimmed_length = len(description.strip())

                if trimmed_length % 3 == 0:
                    item_points = int(math.ceil((price * 0.2)))
                    points += item_points
                    breakdown.append(f'{item_points} points - "{description.strip()}" is {trimmed_length} characters (a multiple of 3)\n'
                                     f"             item price of {price} * 0.2 = {round(price * 0.2, 2)}, rounded up is {item_points} points")

            # Rule 6: 6 points if the day in the purchase date is odd
            _, _, purchase_day = map(int, purchase_date.split('-'))
            if (purchase_day % 2) != 0:
                points += 6
                breakdown.append("6 points - purchase day is odd")

            # Rule 7: 10 points if time of purchase is
            # after 2:00pm and before 4:00pm
            purchase_hour, purchase_min = map(int, purchase_time.split(':'))
            if 14 <= purchase_hour < 16 and purchase_min != 0:
                points += 10
                time = convert_time(purchase_time)
                breakdown.append(f"10 points - {time} is between 2:00pm and 4:00pm")

        else:
            raise ValueError("No receipt!!")

    except Exception as e:
        breakdown.append(f"Error: {str(e)}")

    return points, breakdown
