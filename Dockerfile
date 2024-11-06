# official Python image as the base image
FROM python:3.10-slim

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
