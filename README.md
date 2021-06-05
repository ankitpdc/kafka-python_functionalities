# Kafka Understanding
Refer following link for conceptual part: https://ankit-apdc.gitbook.io/system-design/message-queue/kafka

# Kafka Implementation with Python
kafka-python_functionalities

## Installations
For kafka setup, use docker-compose.yml file within kafka_setup folder. This file will create 3 containers:
1. Zookeeper
2. Broker
3. Schema Registry

To create container, get into the folder kafka_setup and run following command in linux/ubuntu based system:<br />
```console
foo@bar:kafka-python_functionalities/kafka_setup$ docker-compose up -d
```

Install packages in requirements.txt file for using kafka with python. To install, use <br />
```console
foo@bar:kafka-python_functionalities$ pip3 install -r requirements.txt
```

```console
foo@bar:kafka-python_functionalities$ source env.env
```

<strong>Note</strong>: Faced different problems with multiple versions of two packages with Python3.x, mentioned particular versions working perfectly. Tested in production, and working perfectly since more than 1.5 years.

## Folder Structure
app (folder) is the application for all functionalities and example for producing and consuming messages
1. app.py is the entry point
2. kafka_config is for basic configuration (all .env variable are called first in config file only)
3. env.env takes all variables
4. helpers folder contains -
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i. sample avro schema file for example <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ii. kafka functionalities include: creating, listing and deleting topic/topics functionalities <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; iii. consumer functionality file <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; iv. producer functionality file <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; v. For example purpose, created sample data, hence sample_data file is there <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; vi. Always need to apply operations on consumed kafka messages, function inside "use_consumed_msg" can be used for this purpose <br />
		
## Testing:
To test, run app.py
