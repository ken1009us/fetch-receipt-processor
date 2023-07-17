"""
This module contains a CLI program for interacting with the
Fetch Receipt Processor system.

Dependencies:
- json: Provides functions for working with JSON data.
- requests: Allows making HTTP requests to the FastAPI server.

Functions:
- process_receipt(data): Sends a POST request to the FastAPI server to
  process a receipt based on the provided data.
- retrieve_points(receipt_id): Sends a GET request to the FastAPI server
  to retrieve points for a given receipt ID.
- display_menu(): Displays the main menu options to the user.
- process_receipt_menu(): Provides options to the user for
  entering receipt information.
- retrieve_points_menu(): Provides options to the user for retrieve points.
- get_manual_receipt_data(): Prompts the user to manually
  enter receipt information.
- process_receipt_cli(): Handles the process receipt functionality in the CLI.
- retrieve_points_cli(): Handles the retrieve points functionality in the CLI.
- main(): Main routine for the CLI program.

Note: The script assumes that the FastAPI server is running and accessible
      at 'http://localhost:80'. Modify the server URL as needed.

"""

import json
import os
import pyfiglet
import requests

from pathlib import Path
from app.validation import *


def process_receipt(data):
    """
    Sends a POST request to the FastAPI server to process a receipt.

    Parameters:
    - data (dict): The receipt data to be processed, either entered manually
                   or loaded from a JSON file.

    Prints:
    - "Receipt processed." and the generated receipt ID if successful.
    - "Error processing receipt." otherwise.
    """

    try:
        res = requests.post('http://localhost:80/receipts/process',
                            json=data,
                            headers={"Content-Type": "application/json"})
        res.raise_for_status()
        receipt_id = res.json()["id"]
        print("\nReceipt processed.")
        print(f"ID: {receipt_id}")
        print("Please remember this ID for retrieving points.")
    except requests.exceptions.RequestException as e:
        print("\nError processing receipt.")
        print(e)


def retrieve_points(receipt_id):
    """
    Sends a GET request to the FastAPI server to retrieve points
    for a given receipt ID.

    Parameters:
    - receipt_id (str): The ID of the receipt for which to retrieve the points.

    Prints:
    - The total points and breakdown if successful.
    - "Error retrieving points." otherwise.
    """
    try:
        res = requests.get(f'http://localhost:80/receipts/{receipt_id}/points')
        res.raise_for_status()
        points = res.json()['points']
        breakdown = res.json()['breakdown']
        print(f'\nTotal Points: {points}')
        print("Breakdown:")
        for breakdown_item in breakdown:
            print("   " + breakdown_item)
        print("  + ---------")
        print(f"  = {points} points")
        print()
    except requests.exceptions.RequestException as e:
        print("\nError retrieving points.")
        print(e)


def display_menu():
    """
    Displays the main menu options to the user.
    """
    print("\n=== Fetch Receipt Processor System ===")
    print("1. Process Receipt")
    print("2. Retrieve Points")
    print("3. Exit")


def process_receipt_menu():
    """
    Provides options to the user for entering receipt information.
    """
    print("\n--- Process Receipt ---")
    print("1. Manually enter receipt info")
    print("2. Load receipt info from a JSON file")
    print("3. Go back to the main menu")


def retrieve_points_menu():
    """
    Provides options to the user for entering points information.
    """
    print("\n--- Retrieve Points ---")
    print("1. Enter the receipt ID")
    print("2. Go back to the main menu")


def get_manual_receipt_data():
    """
    Prompts the user to manually enter receipt information.
    """
    print("\nEnter receipt information:")
    retailer = input('Retailer: ')
    valid_date = False
    while not valid_date:
        purchase_date = input('Purchase Date: ')
        if validate_date(purchase_date):
            valid_date = True
        else:
            print("\nInvalid input. Please enter a valid date.")

    valid_time = False
    while not valid_time:
        purchase_time = input('Purchase Time: ')
        if validate_date(purchase_time):
            valid_time = True
        else:
            print("\nInvalid input. Please enter a valid time.")

    total = input('Total: ')

    items = []
    try:
        num_items = int(input('Number of items: '))
        for i in range(num_items):
            item_description = input(f'Item {i + 1} Description: ')
            item_price = input(f'Item {i + 1} Price: ')
            items.append({"shortDescription": item_description,
                          "price": item_price})
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
        return get_manual_receipt_data()

    receipt_data = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "total": total,
        "items": items
    }

    if not validate_receipt_data(receipt_data):
        print("\nInvalid input. Please enter a valid receipt.")
        return get_manual_receipt_data()

    return receipt_data


def process_receipt_cli():
    """
    Handles the process receipt functionality in the CLI.
    """
    process_receipt_menu()
    option = input("\nEnter your choice: ")

    if option == '1':
        receipt_data = get_manual_receipt_data()
        process_receipt(receipt_data)
    elif option == '2':
        try:
            print("Enter the path to the JSON file")
            file_path = input("(i.e., ./example/morning-receipt.json): ")
            file_path = os.path.expanduser(file_path)
            p = Path(file_path)
            receipt_data = json.load(open(p))
            process_receipt(receipt_data)
        except FileNotFoundError:
            print("\nFile not found. Please enter a valid file path.")
            process_receipt_cli()
        except json.JSONDecodeError:
            print("\nInvalid JSON file. \
                  Please make sure the file contains valid JSON data.")
            process_receipt_cli()
    elif option == '3':
        return
    else:
        print("\nInvalid choice. Please try again.")


def retrieve_points_cli():
    """
    Handles the retrieve points functionality in the CLI.
    """
    retrieve_points_menu()
    option = input("\nEnter your choice: ")

    if option == '1':
        receipt_id = input("Enter the receipt ID: ")
        retrieve_points(receipt_id)
    elif option == '2':
        return
    else:
        print("\nInvalid choice. Please try again.")


def main():
    """
    Main routine for the CLI program.
    """
    f = pyfiglet.figlet_format("Fetch Rewards", font="slant", width=20)
    print(f)

    while True:
        display_menu()
        choice = input("\nEnter your choice: ")

        if choice == '1':
            process_receipt_cli()
        elif choice == '2':
            retrieve_points_cli()
        elif choice == '3':
            print("\nThank you for using the Fetch Receipt Processor System!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == '__main__':
    main()
