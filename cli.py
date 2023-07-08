"""
This module contains a CLI program for interacting with the Fetch Receipt Processor system.

Dependencies:
- json: Provides functions for working with JSON data.
- requests: Allows making HTTP requests to the FastAPI server.

Functions:
- process_receipt(data): Sends a POST request to the FastAPI server to process a receipt based on the provided data.
- retrieve_points(receipt_id): Sends a GET request to the FastAPI server to retrieve points for a given receipt ID.
- display_menu(): Displays the main menu options to the user.
- process_receipt_menu(): Provides options to the user for entering receipt information.
- retrieve_points_menu(): Provides options to the user for retrieve points.
- get_manual_receipt_data(): Prompts the user to manually enter receipt information.
- process_receipt_cli(): Handles the process receipt functionality in the CLI.
- retrieve_points_cli(): Handles the retrieve points functionality in the CLI.
- main(): Main routine for the CLI program.

Note: The script assumes that the FastAPI server is running and accessible at 'http://localhost:80'. Modify the server URL as needed.

"""

import json
import requests
import pyfiglet

from pathlib import Path


def process_receipt(data):
    """
    Sends a POST request to the FastAPI server to process a receipt.

    Parameters:
    - data (dict): The receipt data to be processed, either entered manually or loaded from a JSON file.

    Prints:
    - "Receipt processed." and the generated receipt ID if successful.
    - "Error processing receipt." otherwise.
    """

    try:
        response = requests.post('http://localhost:80/receipts/process', json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        receipt_id = response.json()["id"]
        print("Receipt processed.")
        print(f"ID: {receipt_id}")
    except requests.exceptions.RequestException as e:
        print("Error processing receipt.")
        print(e)


def retrieve_points(receipt_id):
    """
    Sends a GET request to the FastAPI server to retrieve points for a given receipt ID.

    Parameters:
    - receipt_id (str): The ID of the receipt for which to retrieve the points.

    Prints:
    - The total points and breakdown if successful.
    - "Error retrieving points." otherwise.
    """
    try:
        response = requests.get(f'http://localhost:80/receipts/{receipt_id}/points')
        response.raise_for_status()
        points = response.json()['points']
        breakdown = response.json()['breakdown']
        print(f'Total Points: {points}')
        print("Breakdown:")
        for breakdown_item in breakdown:
            print("   " + breakdown_item)
        print("  + ---------")
        print(f"  = {points} points")
        print()
    except requests.exceptions.RequestException as e:
        print("Error retrieving points.")
        print(e)


def display_menu():
    """
    Displays the main menu options to the user.
    """
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
    print("3. Back")


def retrieve_points_menu():
    """
    Provides options to the user for entering points information.
    """
    print("\n--- Retrieve Points ---")
    print("1. Enter the receipt ID")
    print("2. Back")


def get_manual_receipt_data():
    """
    Prompts the user to manually enter receipt information.
    """
    print("\nEnter receipt information:")
    retailer = input('Retailer: ')
    purchase_date = input('Purchase Date: ')
    purchase_time = input('Purchase Time: ')
    total = input('Total: ')

    items = []
    num_items = int(input('Number of items: '))
    for i in range(num_items):
        item_description = input(f'Item {i + 1} Description: ')
        item_price = input(f'Item {i + 1} Price: ')
        items.append({"shortDescription": item_description, "price": item_price})

    receipt_data = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "total": total,
        "items": items
    }

    return receipt_data


def process_receipt_cli():
    """
    Handles the process receipt functionality in the CLI.
    """
    process_receipt_menu()
    option = input("Enter your choice: ")

    if option == '1':
        receipt_data = get_manual_receipt_data()
        process_receipt(receipt_data)
    elif option == '2':
        file_path = input("Enter the path to the JSON file: ")
        p = Path(file_path)
        receipt_data = json.load(open(p))
        process_receipt(receipt_data)
    elif option == '3':
        return
    else:
        print("Invalid choice. Please try again.")


def retrieve_points_cli():
    """
    Handles the retrieve points functionality in the CLI.
    """
    retrieve_points_menu()
    option = input("Enter your choice: ")

    if option == '1':
        receipt_id = input("Enter the receipt ID: ")
        retrieve_points(receipt_id)
    elif option == '2':
        return


def main():
    """
    Main routine for the CLI program.
    """
    f = pyfiglet.figlet_format("Fetch Rewards", font="slant", width=20)
    print(f)
    print("=== Fetch Receipt Processor System ===")

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            process_receipt_cli()
        elif choice == '2':
            retrieve_points_cli()
        elif choice == '3':
            print("\nThank you for using the Fetch Receipt Processor System!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
