
from helpers.kafka_functionalities import kafka_functionalities
from helpers.producer import AssignValuesAndProduceToKafka
from helpers.consumer import ConsumingKafkaMessage

import time

kafka_functionalities().create_topics(['test-topic', 'test-topic2', 'test-topic3'])
time.sleep(5) # 5 seconds time stop for refresh, broker to get updated

kafka_functionalities().list_topics()
time.sleep(5)

kafka_functionalities().delete_topics(['test-topic2'])
time.sleep(5)

kafka_functionalities().list_topics() # listing again to see if topic is deleted or not
time.sleep(5)

'''Produce Messages to a Topic'''
# Producing a message is bit tricky, you need to prepare three things
# 1. kafka schema for the entity (helpers/avro_schema/sample.avsc)
# 2. Update AssignValuesAndProduceToKafka object to match messsage as per defined avro schema
# 3. Update DataObject object for step 2

# For sample, writing student data as created in file, kafka topic is as defined in .env (test-topic)
from helpers.sample_data import get_student_data
student_data = get_student_data()

ptk = AssignValuesAndProduceToKafka()
for data in student_data:
    ptk.produce_job_information(data)
time.sleep(5)

'''Consume Messages'''
# Consuming a message is straight forward, reading student data from same kafka topic
ConsumingKafkaMessage()