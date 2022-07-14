# Select the base image
FROM fluent/fluent-bit:1.9-debug

WORKDIR /fluent-bit

# Copy the configuration files to the workspace
COPY ./inputs.conf etc/inputs.conf
COPY ./filters.conf etc/filters.conf
COPY ./outputs.conf etc/outputs.conf
COPY ./fluent-bit.conf etc/fluent-bit.conf

