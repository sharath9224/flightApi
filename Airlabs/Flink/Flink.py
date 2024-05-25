from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.descriptors import Schema, Kafka, Json

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

table_env = StreamTableEnvironment.create(env)

kafka_source = Kafka()
kafka_source.version('universal')
kafka_source.topic('airlabs_data')
kafka_source.start_from_earliest()
kafka_source.property('bootstrap.servers', 'localhost:9092')
kafka_source.format('json').schema(Schema().field('data', DataTypes.STRING()))

table_env.connect(kafka_source).in_append_mode().register_table_source('kafka_source')

# Define your data processing logic here

kafka_sink = Kafka()
kafka_sink.version('universal')
kafka_sink.topic('processed_airlabs_data')
kafka_sink.property('bootstrap.servers', 'localhost:9092')
kafka_sink.format('json').schema(Schema().field('data', DataTypes.STRING()))

table_env.connect(kafka_sink).in_append_mode().register_table_sink('kafka_sink')

# Example query - adjust based on your needs
table_env.from_path('kafka_source').insert_into('kafka_sink')

env.execute('flink_job')
