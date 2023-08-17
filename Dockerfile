# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for Python and Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Expose the port that the application will run on
EXPOSE 8000

# Run database migrations and create a superuser
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Add an additional user
RUN echo "from django.contrib.auth.models import User; User.objects.create_user('user', 'user@example.com', 'user')" | python manage.py shell

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
