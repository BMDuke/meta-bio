# Select the base image
FROM fluent/fluent-bit:1.9-debug

WORKDIR /fluent-bit

# Copy the configuration files to the workspace
COPY ./inputs.conf inputs.conf
COPY ./filters.conf filters.conf
COPY ./outputs.conf outputs.conf
COPY ./fluent-bit.conf fluent-bit.conf

