from confluent_kafka.avro.serializer import SerializerError
from kafka_config import unpack, kafka_consumer_config
from helpers.use_consumed_msg import sample_operation_on_consumed_message


###################################################################################################
class ConsumingKafkaMessage():
    def __init__(self, poll_wait_time=10):
        
        print("<<<<<<<< Consumer Initiated >>>>>>>>>>>>>>")
        self.poll_wait_time = int(poll_wait_time)
        self.kafka_consumer, self.topic = kafka_consumer_config()
        self.get_kafka_message()
   

#########################################################################

    def get_kafka_message(self):
        try:
            self.kafka_consumer.subscribe([self.topic])

            while True:
                try:
                    msg = self.kafka_consumer.poll(self.poll_wait_time)
                except SerializerError as e:
                    print("Message deserialization failed for %s: %s", msg, e)
                    raise SerializerError
                except Exception as e:
                    print("An error occured %s", e)
                if msg:
                    if msg.error():
                        print("AvroConsumer error: %s", msg.error())
                        return
                    input_json = unpack(msg.value())
                    try:
                        sample_operation_on_consumed_message(input_json)
                    except Exception as e:
                        print("Failed for input path %s and error: %s", input_json['path'], e)
                else:
                    print("No message received")
  
        finally:
            # Close down consumer to commit final offsets.
            self.kafka_consumer.close()