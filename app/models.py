"""
This module defines the Item and Receipt models using Pydantic.

Dependencies:
- typing: Provides type hints.
- pydantic: A library for data validation and serialization.

Models:
- Item (BaseModel): Represents an item in a receipt.
  - shortDescription (str): The short description of the item.
  - price (str): The price of the item.

- Receipt (BaseModel): Represents a receipt.
  - retailer (str): The retailer name.
  - purchaseDate (str): The purchase date.
  - purchaseTime (str): The purchase time.
  - total (str): The total amount of the receipt.
  - items (List[Item]): A list of Item objects representing the items
    in the receipt.

"""


from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    """
    Represents an item in a receipt.

    Attributes:
    - shortDescription (str): The short description of the item.
    - price (str): The price of the item.
    """
    shortDescription: str
    price: str


class Receipt(BaseModel):
    """
    Represents a receipt.

    Attributes:
    - retailer (str): The retailer name.
    - purchaseDate (str): The purchase date.
    - purchaseTime (str): The purchase time.
    - total (str): The total amount of the receipt.
    - items (List[Item]): A list of Item objects representing the items
      in the receipt.
    """
    retailer: str
    purchaseDate: str
    purchaseTime: str
    total: str
    items: List[Item]
