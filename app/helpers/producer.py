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

    def produce_job_information(self, output_data_list):
        try:
            record = DataObject()

            record.createdOn = output_data_list[0]
            record.Name = output_data_list[1]
            record.dateOfBirth = output_data_list[2]
            record.standard = output_data_list[3]
            record.section = output_data_list[4]
            record.subjects = output_data_list[5]

            # print(record.to_dict())
            self.ptk.produce_message(record.to_dict())
        except Exception as e:
            print("Failed to write to kafka and error: %s", e)


class DataObject(object):
    """
        dataObject stores the deserialized Avro record.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["createdOn", "Name", "dateOfBirth", "standard", "section", "subjects"]

    def __init__(self, createdOn = None, Name = None, dateOfBirth = None, standard = None, section = None, subjects = None):
        
        self.createdOn = createdOn
        self.Name = Name
        self.dateOfBirth = dateOfBirth
        self.standard = standard
        self.section = section
        self.subjects = subjects

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return {
            "createdOn": self.createdOn,
            "Name": self.Name,
            "dateOfBirth": self.dateOfBirth,
            "standard": self.standard,
            "section": self.section,
            "subjects": self.subjects
        }

###########