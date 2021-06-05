from confluent_kafka.avro import AvroProducer
from kafka_config import kafka_producer_config

class ProduceObjectToKafka():
    def __init__(self, record_schema, conf, topic):

        self.record_schema = record_schema
        self.conf = conf
        self.topic = topic

    def on_delivery(self, err, msg, obj):
        if err is not None:
            print('Message delivery to kafka failed, with error {}'.format(err))
        # else:
            # print('Message successfully produced to {} [{}] at offset {}'.format(
                # msg.topic(), msg.partition(), msg.offset()))

    def produce_message(self, record):
        producer = AvroProducer(self.conf, default_value_schema=self.record_schema)
        try:
            producer.produce(topic=self.topic, value=record,
                            callback=lambda err, msg, obj=record: self.on_delivery(err, msg, obj))
            producer.poll(0)
            print("Succefully written to topic: %s", self.topic)
        except ValueError:
            print("Invalid input, discarding record, not written to topic: %s", self.topic)
        
        producer.flush()


class AssignValuesAndProduceToKafka():
    def __init__(self):
        record_schema, conf, topic = kafka_producer_config()
        self.ptk = ProduceObjectToKafka(record_schema, conf, topic)

    def produce_job_information(self, data, input_json):
        try:
            record = DataObject()

            record.senderName = data.get('sender_name')
            record.company = data.get('company')
            record.senderEmail = data.get('sender_email')

            # print(record.to_dict())
            self.ptk.produce_message(record.to_dict())
        except Exception as e:
            print("Failed to write to kafka and error: %s", e)


class DataObject(object):
    """
        dataObject stores the deserialized Avro record.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["senderName", "company", "senderEmail"]

    def __init__(self, senderName = None, company = None, senderEmail = None):
        
        self.senderName = senderName
        self.company = company
        self.senderEmail = senderEmail

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return {
            "sourceOfJob": "email",
            "senderName": self.senderName,
            "company": self.company
        }

###########