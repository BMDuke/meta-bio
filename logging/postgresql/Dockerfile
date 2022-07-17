# Select base image
FROM postgres:14

# Copy init.sh script to db init directory
COPY ./init.sh /docker-entrypoint-initdb.d/init.sh

# Copy back up script to grant user access
COPY ./grant.sh /grant.sh