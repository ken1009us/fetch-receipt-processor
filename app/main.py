"""
This module defines an API using FastAPI for processing receipts
and calculating points.

Endpoints:
- POST /receipts/process: Generates a receipt ID for a given receipt.
- GET /receipts/{id}/points: Retrieves the points and breakdown
  for a given receipt ID.

Dependencies:
- fastapi: The FastAPI framework for building APIs.
- models: Contains the Item and Receipt models used in the API.
- utils: Provides helper functions for generating receipt IDs
  and calculating points.

Global Variables:
- db.uuid_dict: A dictionary to store receipt IDs and their corresponding
  Receipt objects.

Functions:
- get_receipt_id(receipt: Receipt): Generates a receipt ID for a given receipt
  and stores it in db.uuid_dict.
- get_points(id: str): Retrieves the points and breakdown for a given
  receipt ID from db.uuid_dict.

"""

from db import db
from fastapi import FastAPI, HTTPException
from .models import Receipt
from .utils import generate_receipt_id, calculate_points


app = FastAPI()


@app.post("/receipts/process")
def get_receipt_id(receipt: Receipt):
    """
    Generates a receipt ID for a given receipt and stores it in db.uuid_dict.

    Parameters:
    - receipt (Receipt): The receipt object containing the receipt information.

    Returns:
    - dict: A dictionary containing the generated receipt ID.
    """
    id = generate_receipt_id()
    db.uuid_dict[id] = [receipt]
    points, breakdown = calculate_points(id, db.uuid_dict)
    db.uuid_dict[id].append((points, breakdown))
    return {"id": id}


@app.get("/receipts/{id}/points")
def get_points(id: str):
    """
    Retrieves the points and breakdown for a given receipt ID from db.uuid_dict.

    Parameters:
    - id (str): The receipt ID for which to retrieve the points.

    Returns:
    - dict: A dictionary containing the points and breakdown information
            for the receipt ID.
    """
    if id not in db.uuid_dict:
        raise HTTPException(status_code=404, detail="Receipt ID not found.")
    points = db.uuid_dict[id][1][0]
    breakdown = db.uuid_dict[id][1][1]
    return {"points": points, "breakdown": breakdown}
