# Select base image
FROM python:3.10.4

# Create a working directory
WORKDIR /rmq_worker

# Copy files across
COPY ./database ./database
COPY ./rabbitmq ./rabbitmq
COPY ./requirements.txt ./

# Set up env vars
# ENV DB_URL ${SQLALCHEMY_DATABASE_URL}

# Install required packages
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Run the start commands
CMD ["python", "-m", "rabbitmq.RMQConsumer"]
