# Receipt Processing and Points Calculation

This repository contains a set of Python scripts and modules for processing receipts, generating receipt IDs, and calculating points based on receipt information. The system is built using the FastAPI framework and utilizes Pydantic for data validation.

## Prerequisites

- Python 3.11.4
- Required packages: `fastapi`, `uvicorn`, `pydantic`, `requests`

## Installation

1. Clone this repository:

```bash
$ git clone https://github.com/ken1009us/fetch-receipt-processor.git
```

2. Install the required packages using pip:

```bash
$ pip install -r requirements.txt
```

## Usage

### Option1: Terminal

1. Start the FastAPI server:

```bash
$ uvicorn app.main:app --reload
```

2. Use the Command Line Interface script to interact with the server:

```bash
$ python3 cli.py
```

The cli script provides a menu-driven interface to process receipts and retrieve points. It allows you to manually enter receipt information or provide a path to a JSON file containing the receipt data.

### Option2: Docker

1. Make sure you have Docker installed on your system. You can download and install Docker from the official Docker website: https://www.docker.com/.

2. Navigate to the project directory in your terminal.

3. Build the Docker image using the following command:

```bash
$ docker build -t receipt-processor .
```

This command builds a Docker image with the name receipt-processor based on the Dockerfile in the current directory. The -t flag specifies the image name.

4. After the image is built successfully, you can run a Docker container using the image with the following command:

```bash
$ docker run -d --name mycontainer -p 80:80 receipt-processor
```

The docker run command creates and starts a new Docker container from the receipt-processor image. The -d flag runs the container in detached mode (in the background), --name specifies a name for the container, and -p maps the container's port 80 to the host's port 80, allowing access to the FastAPI server.

5. Use the Command Line Interface script to interact with the server:

```bash
$ python3 cli.py
```


## Files

```
- main.py: The main FastAPI server script that defines the API endpoints and handles receipt processing and points calculation.
- models.py: Contains the Pydantic models for the Item and Receipt objects used in the API.
- utils.py: Utility functions for generating receipt IDs, decoding IDs, converting time, and calculating points.
- cli.py: A command line interface script that interacts with the FastAPI server to process receipts and retrieve points.
- README.md: This file, providing an overview of the repository and usage instructions.
```

## Contributing

Contributions to this repository are welcome. If you find any issues or have suggestions for improvements, please create a new issue or submit a pull request.

