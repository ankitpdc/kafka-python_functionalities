
import os
home_path = os.path.expanduser('~')
home = os.path.abspath(os.path.join(home_path))


BOOTSTRAP_SERVERS = 'localhost:19092'
SCHEMA_REGISTRY_URL= 'http://localhost:7070'
GROUP_ID= 'groupid101'
AUTO_OFFSET_RESET = None

if not AUTO_OFFSET_RESET:
    AUTO_OFFSET_RESET= 'earliest'
CONSUMER_TOPIC = 'test-topic'
PRODUCE_TOPIC = 'test-topic'

def kafka_schema():
    ''' Parse Schema used for serializing class '''
        # Note that here we are using avro.loads not avro.load
        # use avro.load when trying to read .avsc avro schema file
        # This is sample schema for kafka with python, we will not be using this function
        # rather we will load .avsc file for our purpose

    
    from confluent_kafka import avro

    record_schema = avro.loads("""
        {
            "namespace": "resumeLinks",
            "name": "links",
            "type": "record",
            "fields": [
                {"name": "name", "type": "string"}
            ]
        }
    """)
    return record_schema

def kafka_bootstrap_servers():
    return BOOTSTRAP_SERVERS
    

def kafka_producer_config():
    from confluent_kafka import avro
    record_schema = avro.load(str(home) + '/helpers/avro_schema/sample.avsc')

    conf = {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'schema.registry.url': SCHEMA_REGISTRY_URL}
    output_produce_topic = PRODUCE_TOPIC
    return record_schema, conf, output_produce_topic


def unpack(payload):
    ''' avro to json format converter '''
        # This function will be used while consuming the kafka message
        # The format of the kafka message is .avsc (.avro for java)
        # It converts incoming messages into json (dictionary) format
    
        # Input is the complete payload, single kafka message

    import struct
    import io
    from avro.io import BinaryDecoder, DatumReader
    from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

    register_client = CachedSchemaRegistryClient(url=SCHEMA_REGISTRY_URL)

    MAGIC_BYTES = 0
    magic, schema_id = struct.unpack('>bi', payload[:5])
    # Get Schema registry
    # Avro value format
    if magic == MAGIC_BYTES:
        schema = register_client.get_by_id(schema_id)
        reader = DatumReader(schema)
        output = BinaryDecoder(io.BytesIO(payload[5:]))
        abc = reader.read(output)
        return abc
    # String key
    else:
        # Timestamp is inside my key
        return payload[:-8].decode()

def kafka_consumer_config():
    
    from confluent_kafka import Consumer

    consumer = Consumer({
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': GROUP_ID,
            'auto.offset.reset': AUTO_OFFSET_RESET,
            'enable.auto.commit': True
        })
    input_consumer_topic = CONSUMER_TOPIC

    return consumer, input_consumer_topic