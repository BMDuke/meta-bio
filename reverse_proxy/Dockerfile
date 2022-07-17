# Select the base image
FROM nginx

# Copy files into container
COPY ./embl.conf /etc/nginx/conf.d/embl.conf
COPY ./landing.html /usr/share/nginx/html/landing.html

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Insert envars into config 
# RUN envsubst < /etc/nginx/conf.d/embl.conf > tmp.conf \
#         && mv tmp.conf /etc/nginx/conf.d/embl.conf

# Define startup 
# CMD ["/bin/sh" , "-c" , "envsubst < /etc/nginx/conf.d/embl.conf && exec nginx -g 'daemon off;'"]