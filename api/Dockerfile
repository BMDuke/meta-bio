# Select base image
FROM python:3.10.4

# Create new user to allow Jenkins to run tests
ARG GID
ARG UID
ARG UNAME

ENV GROUP_ID=$GID
ENV USER_ID=$UID
ENV USERNAME=$UNAME

RUN mkdir -p /api/$USERNAME

RUN groupadd -g $GROUP_ID $USERNAME
RUN useradd -r -u $USER_ID -g $USERNAME -d /api/$USERNAME $USERNAME
RUN chown $USERNAME:$USERNAME /api/$USERNAME

USER $USERNAME
WORKDIR /api/$USERNAME

# Create a working directory
# WORKDIR /api

# Copy files across
COPY ./app/ ./app
COPY ./database ./database
COPY ./requirements.txt ./

# Set up env vars
# ENV DB_URL ${SQLALCHEMY_DATABASE_URL}

# Install required packages - https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


# Run the start commands
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/api/v1/"]
