
from helpers.kafka_functionalities import create_topics, list_topics, delete_topics
from helpers.producer import AssignValuesAndProduceToKafka
from helpers.consumer import ConsumingKafkaMessage



create_topics()
list_topics()
delete_topics()
AssignValuesAndProduceToKafka()
ConsumingKafkaMessage()