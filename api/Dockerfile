# Select base image
FROM python:3.10.4

# Create a working directory
WORKDIR /api

# Copy files across
COPY ./app/ ./app
COPY ./database ./database
COPY ./requirements.txt ./
COPY ./.env ./.env 

# Set up env vars
# ENV DB_URL ${SQLALCHEMY_DATABASE_URL}

# Install required packages
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Run the start commands
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/api"]
