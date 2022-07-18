# EMBL Metadata REST API Challege

## Table of Contents
1. [Example](#example)
2. [Example2](#example2)
3. [Third Example](#third-example)
4. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)

## Release Notes
### Known Issues
- Grafana data base access: Log into postgres and grant user embl_grafana access
- Grafana log in: chown 472:472 gf_data dir
- Jenkins 502: Restart container
- api_v2 502: Ensure rabbitmq server is up and running, then restart container
- Grafana: 502

## About
This is an API service designed to help people find information about databses related to a given organism in the main Ensemble database. This API provides a single endpoint to search for datasets. It accepts the following arguments as query parameters:
- name: Organism name
- db_type: The type of dataset. eg. cdna
- release: The release number to filter on 

## Installation
### Requirements
- Docker version 20.10.8+
- Docker Compose version 2.5.0+

### Project set up
Go to a location that you would like to use as your project workspace and create a new directory to contain all the project files.
```
mkdir emblAPI
```
Then enter that directory.
```
cd emblAPI
```
Initialise a new git repository
```
git init
```
Then clone the repo into your local filespace
```
git pull https://github.com/BMDuke/meta-bio.git
```
Next we need to configure our environment a little bit. There are two things we need to do:
- **Change permissions on docker socket**: This deployment uses Jenkins as a CICD server and as part of our build process we will need to use Jenkins to build images for us. We install docker in the Jenkins image, however, rather than run docker-in-docker, we just mount the docker socket on the **host** into the container using a bind mount. More information about this can be found [here](http://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/). 
- **Change ownership of the jenkins volume**: This deployment comes with stateful volumes for Jenkins, RabbitMQ and Grafana services. This has allowed snapshots of their configuration to be taken which can not be resumed when the project is deployed.

To change permissions on the docker socket:
```
sudo chmod 666 /var/run/docker.sock
```

And for Grafana:
```
sudo chown -R 472:472 logging/grafana/gf_data/
```

### Installation
Now we are ready to build the images.
```
sudo docker-compose build
```

And finally we can launch the containers.
```
sudo docker-compose up -d
```

### Nest steps
If you have had any problems, sheck out the trouble shooting section.
If you're all set with no problems, check out the usage section. 

## Usage
The service has a main entry point at [`http://localhost/`](http://localhost/) which provides links to each of the services via a minimal UI.

### Calling the API 


## Contact







Connecting docker to on host machine to docker in jenkins requires bind mounting the docker runtime to that on the jenkins container.
For this to work you may need to grant permissions for this on the host machine by runinning 


And for grafana
sudo chown -R 472:472 logging/grafana/gf_conf/

## Troubleshooting


```
The PostgreSQL permission fix
*****************************

If you cannot view any of the log data in the /grafana/ dashboard, it is likely that the user permissions have failed to be applied successfully on the postgresql image build. To fix this.

# Have a look at which containers are running and which are crashing. 
# Copy the container id of the container running postgresql. 

sudo docker container ls 

# Then with the container id copied to clipboard, run

sudo docker exec -it <container id> bash

# Now we want to invoke the postgres CLI. Run the following command and when prompted, enter 'password' as the password.

psql -h postgres -U embl

# We need to select the service_monitoring database

\c service_monitoring

# Have a look at the tables

\dt

# Optionally, you can check to see if logs are successfully making their way there.

SELECT * FROM application_logs LIMIT 5;

Now, check that the embl_grafana user exists. They should appear in the table.

\du+

# Next, we need to give them permissionto connect to the database and select information from it. Run the following

GRANT CONNECT ON DATABASE service_monitoring TO embl_grafana;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO embl_grafana;

# Now this should have have fixed the issue. Exit out of the postgres cli and the container

exit
...
exit

# Now we need to restart the container. Using the same container id that you used a moment ago to access the postgres container;

sudo docker restart <container id>

# Now make sure it works. Naviagte to localhost/grafana and view the monitoring dashboard.

```

