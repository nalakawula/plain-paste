# Use the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /var/www/app

# Set dir permissions
RUN chown -R www-data:www-data /var/www

# Set the user to use when running this image
USER www-data

# Copy the requirements file to the container
COPY --chown=www-data:www-data requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY --chown=www-data:www-data . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Start the FastAPI server
CMD ["/var/www/.local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]