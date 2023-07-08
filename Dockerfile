# Use an official Python runtime as the base image
FROM python:3.11.4

# Set the working directory inside the container
WORKDIR /code

# Create and activate the virtual environment
RUN python -m venv .venv
ENV PATH="/code/.venv/bin:$PATH"

# Copy the requirements.txt file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install the required packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the project files to the working directory
COPY ./app /code/app

# Expose the port on which the FastAPI server runs (default is 8000)
EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/code/app"

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]