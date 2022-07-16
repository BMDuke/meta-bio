# Select the base image
FROM nginx

# Copy files into container
COPY ./embl.conf /etc/nginx/conf.d/embl.conf
COPY ./landing.html /var/www/embl.metadata/landing.html

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

