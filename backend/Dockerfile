FROM python:3.8-slim

# Set the working directory to /app
ENV FLASK_APP /backend/app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development


# Copy the current directory contents into the container at /app
COPY ./requirements.txt ./backend/

# Install any needed packages specified in requirements.txt
RUN pip install -r ./backend/requirements.txt

# Define environment variable
COPY . ./backend

ENTRYPOINT ["/backend/entrypoint.sh"]