# Receipt Processing and Points Calculation

```bash
    ______     __       __       ____                              __
   / ____/__  / /______/ /_     / __ \___ _      ______ __________/ /____
  / /_  / _ \/ __/ ___/ __ \   / /_/ / _ \ | /| / / __ `/ ___/ __  / ___/
 / __/ /  __/ /_/ /__/ / / /  / _, _/  __/ |/ |/ / /_/ / /  / /_/ (__  )
/_/    \___/\__/\___/_/ /_/  /_/ |_|\___/|__/|__/\__,_/_/   \__,_/____/


=== Fetch Receipt Processor System ===
1. Process Receipt
2. Retrieve Points
3. Exit
```

This repository contains a set of Python scripts and modules for processing receipts, generating receipt IDs, and calculating points based on receipt information. The system is built using the FastAPI framework and utilizes Pydantic for data validation.

## Prerequisites

- Python
- Required packages: `fastapi`, `uvicorn`, `pydantic`, `requests`, `pyfiglet`

## Installation

1. Clone this repository:

```bash
$ git clone https://github.com/ken1009us/fetch-receipt-processor.git
```

2. Navigate to the project directory:

```bash
$ cd fetch-receipt-processor
```

3. Installing Python

NOTE: Before proceeding with the installation of the Python and pip, ensure that they are installed on your system. If you already have them installed, you can skip these steps.

a. Visit the official Python website at [python.org](https://www.python.org/).\
b. Download the latest version of Python for your operating system.\
c. Run the installer and follow the instructions to install Python.\
d. Make sure to select the option to add Python to your system's PATH during the installation process.

4. Installing pip

Pip is a package management system used to install and manage Python packages. It is usually installed by default with Python. To verify if pip is installed, open a terminal/command prompt and run the following command:

```bash
$ pip --version
```

If pip is not installed or you have an older version, follow the steps below to install or upgrade it.

a. Open a terminal/command prompt.
b. Run the following command to install or upgrade pip:

```bash
$ python -m ensurepip --upgrade
```

For Windows:

```bash
C:> py -m ensurepip --upgrade
```

5. Run the following command to install nox:

NOTE: ONLY for the user who choose NOT to utilize Docker, if you want to use Docker, there is no need to install nox. You can directly proceed to the section [Usage Option 1: Docker](#usage)


```bash
$ pip3 install nox
```

This will download and install the latest version of nox from the Python Package Index (PyPI).

## Nox Setup

NOTE: ONLY for the user who choose NOT to utilize Docker

After installing nox, you can set it up and activate the virtual environment by following these steps:

NOTE: Only for the user who choose NOT to utilize Docker.

1. Ensure you are in the root directory of your project.

2. Open a command prompt or terminal window.

3. Run the following command to set up the project:

```bash
$ nox -s setup
```

4. Once the setup session completes successfully, you can activate the virtual environment by running the following command:

```bash
$ source .nox/setup/bin/activate
```

This command activates the virtual environment created by nox specifically for your project.

Note: The source command is specific to Unix-like systems (e.g., Linux or macOS). If you're using a different operating system, please refer to the appropriate command to activate a virtual environment. EX: `nox\Scripts\activate.bat`.

5. After activating the virtual environment, you can now run additional commands or scripts within the project's isolated environment. This ensures that the dependencies and configuration set up during the setup session are available.

## Usage

### Option 1: Docker (DEFAULT)

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

5. Run the following command to install pyfiglet:

```bash
$ pip3 install pyfiglet==0.7
```

Pyfiglet is a Python library that allows us to create ASCII art from text. I used it in CLI to enhance the visual presentation of text-based outputs.

6. Use the Command Line Interface script to interact with the server:

```bash
$ python3 cli.py
```

The cli script provides a menu-driven interface to process receipts and retrieve points. It allows you to manually enter receipt information or provide a path to a JSON file containing the receipt data.

### Option 2: Terminal

NOTE: If you want to test the app locally without using Docker, you'll need to make a slight adjustment to the URL. Instead of http://localhost:80, please use http://localhost:8000.

1. Navigate to the project directory in your terminal

2. Before proceeding, make sure to fully install and set up Nox, and then activate the environment

3. Start the FastAPI server:

```bash
$ uvicorn app.main:app --reload
```

4. Launch a new terminal window or tab and navigate to the project directory

5. Use the Command Line Interface script to interact with the server:

```bash
$ source .nox/setup/bin/activate

$ python3 cli.py
```

## Files

- main.py: The main FastAPI server script that defines the API endpoints and handles receipt processing and points calculation.
- models.py: Contains the Pydantic models for the Item and Receipt objects used in the API.
- utils.py: Utility functions for generating receipt IDs, decoding IDs, converting time, and calculating points.
- cli.py: A command line interface script that interacts with the FastAPI server to process receipts and retrieve points.
- db.py: In-memory database.
- validation.py: This module provides functions for validating date, time, and receipt data.
- noxfile.py: This script sets up a virtual environment, installs required packages, and performs linting using Flake8.
- README.md: This file, providing an overview of the repository and usage instructions.

## Contributing

Contributions to this repository are welcome. If you find any issues or have suggestions for improvements, please create a new issue or submit a pull request.
