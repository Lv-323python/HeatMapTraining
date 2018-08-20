# HeatMapTraining

Project description goes here ...

## Getting Started

These instructions will get you a copy of the application up and running on your local machine for development and testing purposes. 
See installing and running the application for detailed notes on how to install and run the application.

### Prerequisites

Before running the application **make sure that *docker* and *docker-compose* are installed on your machine**. If not follow the [***docker***](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce) and [***docker-compose***](https://docs.docker.com/compose/install/#install-compose) installation guides. 


### Installing

To get the working copy of the application clone or download [***HeatMapTraining***](https://github.com/Lv-323python/HeatMapTraining) repository. 


## Running the application
Running with ***docker-compose*** :
1. Open the terminal and navigate to ***HeatMapTraining*** folder.
2. Start up the application by running ```sudo docker-compose up```.
3. Enter http://0.0.0.0:8000/ in a browser to see the application running.
4. Stop the application, either by running ```sudo docker-compose down``` from within your project directory in the second terminal, or by hitting ```CTRL+C``` in the original terminal where you started the app.

**Note:** if you just want to run the application in ***PyCharm*** (without ***docker-compose***) 
1. Run the rabbitmq server in ***docker container*** by typing:

```
sudo docker run -d --name container_name -p rabbitmq_server_port:5672 -p management_plugin_port:15672 rabbitmq:3-management
```
Parameters:
- *container_name*  -  the name ***container*** will get after creation
- *rabbitmq_server_port* - the port on which ***rabbitmq server*** will be running 
- *management_plugin_port* - the port on which ***rabbitmq management plugin*** will be running

2. Change ```HOST = 'localhost'``` and ```PORT = rabbitmq_server_port``` in the ```producer/rabbitmq_helpers/request_sender_client_config.py``` and ```consumer/helper/consumer_config.py``` files.

Parameters:
- *rabbitmq_server_port* - should be the port on which ***rabbitmq server*** is running on your local mahcihe.

3. Open ***consumer*** project in ***PyCharm*** and run ```receiver.py```.
4. Open ***producer*** project in ***PyCharm*** and run  ```client.py```.


## View Log files:
1. To view the general ***log*** file in real time, just use the command below:
```
cd /data && tail -f $(ls data.*.log -t1 |  head -n 1) | sed 's/\n/n/g;G;G'
```
**Note:** use this command only after the ***app*** has been successfully started using the ***docker-compose*** file .




