# ---- Base Stage ----
# Use an official lightweight Python image
FROM python:3.9-slim as base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ---- Final Stage ----
# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application using Gunicorn
# This is a robust way to run a Flask app in production.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
