"""
This module defines functions to process receipts and retrieve points using a FastAPI server.

Functions:
- process_receipt(data): Sends a POST request to the FastAPI server to process a receipt.
- retrieve_points(receipt_id): Sends a GET request to the FastAPI server to retrieve points for a given receipt ID.

Main Routine:
- The main routine provides a menu-driven interface to interact with the functions.
  - Option 1: Process Receipt
    - Allows the user to manually enter receipt information or provide a path to a JSON file.
    - Sends the receipt data to the FastAPI server for processing.
  - Option 2: Retrieve Points
    - Prompts the user to enter a receipt ID.
    - Sends a request to the FastAPI server to retrieve the points and breakdown for the specified receipt ID.
  - Option 3: Exit
    - Terminates the program.

Dependencies:
- json: Provides functions for working with JSON data.
- requests: Allows sending HTTP requests.
- pathlib: Provides classes to work with file paths.

"""


import json
import requests


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
    response = requests.post('http://localhost:8000/receipts/process', json=data, headers={"Content-Type":"application/json"})
    if response.status_code == 200:
        receipt_id = response.json()["id"]
        print("Receipt processed.")
        print(f"ID: {receipt_id}")
    else:
        print("Error processing receipt.")


def retrieve_points(receipt_id):
    """
    Sends a GET request to the FastAPI server to retrieve points for a given receipt ID.

    Parameters:
    - receipt_id (str): The ID of the receipt for which to retrieve the points.

    Prints:
    - The total points and breakdown if successful.
    - "Error retrieving points." otherwise.
    """
    response = requests.get(f'http://localhost:8000/receipts/{receipt_id}/points')
    if response.status_code == 200:
        points = response.json()['points']
        breakdown = response.json()['breakdown']
        print(f'Total Points: {points}')
        print("Breakdown:")
        for breakdown_item in breakdown:
            print("   " + breakdown_item)
        print("  + ---------")
        print(f"  = {points} points")
    else:
        print('Error retrieving points.')


if __name__ == '__main__':
    while True:
        print("1. Process Receipt")
        print("2. Retrieve Points")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            receipt_data = {}
            print("1. Manually type the info")
            print("2. Provide the path to JSON file")
            option = input("Enter your choice: ")

            if option == '1':
                receipt_data = {
                    "retailer": input('Retailer: '),
                    "purchaseDate": input('Purchase Date: '),
                    "purchaseTime": input('Purchase Time: '),
                    "total": input('Total: '),
                    "items": []
                }

                num_items = int(input('Number of items: '))
                for i in range(num_items):
                    item = {
                        "shortDescription": input(f'Item {i + 1} Description: '),
                        "price": input(f'Item {i + 1} Price: ')
                    }
                    receipt_data["items"].append(item)

            elif option == '2':
                file_path = input("JSON file Path: ")
                p = Path(file_path)
                receipt_data = json.load(open(p))

            process_receipt(receipt_data)

        elif choice == '2':
            receipt_id = input("Enter the receipt ID: ")
            retrieve_points(receipt_id)


        elif choice == '3':
            print("Thank you! Bye!")
            break

        else:
            print("Invalid choice. Please try again...")




