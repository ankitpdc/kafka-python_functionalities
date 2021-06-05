
from confluent_kafka.admin import AdminClient, NewTopic
from kafka_config import kafka_bootstrap_servers

class kafka_functionalities():
    def __init__(self):
        bootstrap_servers = kafka_bootstrap_servers()
        self.kafka_instance = AdminClient({'bootstrap.servers': bootstrap_servers})

    def create_topics(self, topics, num_partitions=3, replication_factor=1):
        """ Create topics """
           # topics is a list, 
           # all the topics will be created with num_partition and replication_factor in input
        

        new_topics = [NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor) for topic in topics]
        # Call create_topics to asynchronously create topics, a dict
        # of <topic,future> is returned.
        fs = self.kafka_instance.create_topics(new_topics)

        # Wait for operation to finish.
        # Timeouts are preferably controlled by passing request_timeout=15.0
        # to the create_topics() call.
        # All futures will finish at the same time.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))


    def list_topics(self):
        """ list topics and cluster metadata """

        # if len(args) == 0:
        #     what = "all"
        # else:
        #     what = args[0]

        md = self.kafka_instance.list_topics(timeout=10)
        print("Cluster {} metadata (response from broker {}):".format(md.cluster_id, md.orig_broker_name))

        what='all'
        if what in ("all", "brokers"):
            print(" {} brokers:".format(len(md.brokers)))
            for b in iter(md.brokers.values()):
                if b.id == md.controller_id:
                    print("  {}  (controller)".format(b))
                else:
                    print("  {}".format(b))

        if what not in ("all", "topics"):
            return

        print(" {} topics:".format(len(md.topics)))
        for t in iter(md.topics.values()):
            if t.error is not None:
                errstr = ": {}".format(t.error)
            else:
                errstr = ""

            print("  \"{}\" with {} partition(s){}".format(t, len(t.partitions), errstr))

            for p in iter(t.partitions.values()):
                if p.error is not None:
                    errstr = ": {}".format(p.error)
                else:
                    errstr = ""

                print("    partition {} leader: {}, replicas: {}, isrs: {}".format(
                    p.id, p.leader, p.replicas, p.isrs, errstr))


    def delete_topics(self, topics):
        """ delete topics """

        # Call delete_topics to asynchronously delete topics, a future is returned.
        # By default this operation on the broker returns immediately while
        # topics are deleted in the background. But here we give it some time (30s)
        # to propagate in the cluster before returning.
        #
        # Returns a dict of <topic,future>.

        fs = self.kafka_instance.delete_topics(topics, operation_timeout=30)

        # Wait for operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} deleted".format(topic))
            except Exception as e:
                print("Failed to delete topic {}: {}".format(topic, e))