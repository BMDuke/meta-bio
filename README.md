# EMBL Metadata REST API Challege

## Table of Contents
1. [Release Notes](#release-notes)
2. [About](#about)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contact](#contact)
6. [Troubleshooting](#troubleshooting)

## Release Notes
### Known Issues
- Grafana dashboard fails to load data. See [fix](#the-postgresql-permission-fix).
- Grafana unavailable, server returns 502. See [fix](#502-error-from-grafana).
- General container unavailability, server returns 502. See [fix](#).
- Disconnects. See [fix](#).

## About
This is an API service designed to help people find information about databses related to a given organism in the main Ensemble database. This API provides a single endpoint to search for datasets. It accepts the following arguments as query parameters:
- name: Organism name
- db_type: The type of dataset. eg. cdna
- release: The release number to filter on 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/rabbitmq_config/static/architecture.png?raw=true)

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

And next we can launch the containers.
```
sudo docker-compose up -d
```
Finally, let's make sure our API is passing its tests.
```
sudo docker exec -it metadata_api bash -c pytest
```

### Next steps
If you have had any problems, sheck out the trouble shooting section.
If you're all set with no problems, check out the usage section. 

## Usage
The service has a main entry point at [`http://localhost/`](http://localhost/) which provides links to each of the services via a minimal UI.

### Calling the API 
To call the regular API. Select the first option from the list of options `Metadata API v1`. 
![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/EMBL-MetaData-API.png?raw=true)

This will take you to the swagger ui. Here, expand the drop down and experiment with the Emsembl metadata API. 
![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/FastAPI-Swagger-UI%20(1).png?raw=true)

Query responses are displayed below.
![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/FastAPI-Swagger-UI%20(2)1.png?raw=true)

### Calling the API using a queue-intermediated backend
To call the queue serviced backend, we need to select the second version of the API - `Metadata API v2`. At the same time, we can watch the messages pass through the exchange to the worker by openening the rabbitmq app as well. 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/EMBL-MetaData-API-1.png?raw=true)

In one tab make some requests to the metadata API just like we did in the previous example, then switch to the rabbitMQ tab to see the events. You can find out more information about the process by toggling the tabs. 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/RabbitMQ-Management.png?raw=true)

## Exploring the CICD pipline
To view the CICD pipeline, you will need to select the link to the Jenkins server. 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/EMBL-MetaData-API3.png?raw=true)

After logging in you will be taken to the dashboard where you can see the existing pipelines. Here you can run the pipeline (it will fail) or see more details about it. 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/Dashboard-Jenkins-.png?raw=true)

## Logging and monitoring
The final option from the root page is the logging and monitoring stack, visualised using grafana. 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/EMBL-MetaData-API4.png?raw=true)

From the homepage, select the dashboard option from the left menu and find the `Monitoring` dashboard. 

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/main/static/Home-Grafana.png?raw=true)

Here you will be able to view the logs and recource consumption as the system runs.

![Select api version 1 link](https://github.com/BMDuke/meta-bio/blob/rabbitmq_config/static/FastAPI-Swagger-UI_(2).png?raw=true)

If you have any problems here with data not being displayed, see the troubleshooting section for postgres fixes. 

## Contact

Shoot me a message at duke@bmdanalytics.co.uk :v:


## Troubleshooting

### The PostgreSQL permission fix
If you cannot view any of the log data in the /grafana/ dashboard, it is likely that the user permissions have failed to be applied successfully on the postgresql image build. To fix this.
<br/><br/>
Have a look at which containers are running and which are crashing. Copy the container id of the container running postgresql. 
```
sudo docker container ls 
```
Then with the container id copied to clipboard, run
```
sudo docker exec -it <container id> bash
```
We are going to use the `psql` utility in the postgres image to manually give the `embl_grafana` user `CONNECT` and `SELECT` permissions. Now we want to invoke the postgres CLI. Run the following command and when prompted, enter 'password' as the password.

```
psql -h postgres -U embl
```
We need to select the service_monitoring database

```
\c service_monitoring
```

Have a look at the tables

```
\dt
```

Optionally, you can check to see if logs are successfully making their way there.

```
SELECT * FROM application_logs LIMIT 5;
```

Now, check that the embl_grafana user exists. They should appear in the table.

```
\du+
```
Next, we need to give them permission to connect to the database and select information from it. Run the following

```
GRANT CONNECT ON DATABASE service_monitoring TO embl_grafana;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO embl_grafana;
```
Now this should have have fixed the issue. Exit out of the postgres cli and the container

```
sudo docker restart <container id>
```

Now make sure it works. Naviagte to localhost/grafana and view the monitoring dashboard.


### 502 Error from grafana
This is most likely a permission error. Make sure that you have run 
```
sudo chown -R 472:472 logging/grafana/gf_data/
```
Then restart the service and try again
```
sudo docker-compose down
sudo docker-compose up -d
```
### General container unavailability, server returns 502
This can happen when an error occurs in a container and results in an error progarating between services. As a result containers may rest in a blocked state. To fix this, restart a container individually, restart the service, or pull the service down and redeploy it.
```
sudo docker restart <container id>

OR

sudo docker-compose restart

OR

sudo docker-compose down
sudo docker-compose up -d
```


### Disconnects
After a period of idleness, connections are sometimes dropped. This happens especially frequently with conmponents who are connected to a queue. To fix this, restart a container individually, restart the service, or pull the service down and redeploy it.
```
sudo docker restart <container id>

OR

sudo docker-compose restart

OR

sudo docker-compose down
sudo docker-compose up -d
```
