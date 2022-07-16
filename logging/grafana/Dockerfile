#Select the base image
FROM grafana/grafana-oss

# Copy the config into the container
COPY ./grafana.conf conf/defaults.ini

# Install grafana plugins
RUN grafana-cli plugins install simpod-json-datasource