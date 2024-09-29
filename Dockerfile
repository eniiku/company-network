# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=company_network.settings

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system --deploy

# Copy the project code into the container
COPY . /app/

# Create a directory for static files
RUN mkdir -p /app/staticfiles

# Set permissions for the static files directory
RUN chmod -R 755 /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application
CMD sh -c "python manage.py populate_db && gunicorn --bind 0.0.0.0:8000 company_network.wsgi:application"