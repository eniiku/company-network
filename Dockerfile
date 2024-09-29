# Base image
FROM python:3.12.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=company_network.settings

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt /app/

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Create a directory for static files
RUN mkdir -p /app/staticfiles

# Set permissions for the static files directory
RUN chmod -R 755 /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/health/ || exit 1

# Run the application
CMD sh -c "python manage.py migrate && python manage.py populate_db && gunicorn --workers=3 --bind 0.0.0.0:8000 company_network.wsgi:application"