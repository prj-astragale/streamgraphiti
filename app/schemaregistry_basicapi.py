from confluent_kafka.schema_registry.schema_registry_client import Schema, SchemaReference, SchemaRegistryClient
import fastavro
import logging
import json
logging.basicConfig(level=logging.INFO)


class InlkSchemaRClient():
    def __init__(self) -> None:
        self.url    = None

    async def connect_sr(self, conf):
        self.url    = conf['url']
        self.sr     = SchemaRegistryClient(conf=conf)

    def check_existence(self, subject_name: str) -> bool:
        list_of_schemas = [subject for subject in self.sr.get_subjects()]
        if subject_name in list_of_schemas:
            return True
        else:
            return False
    
    def validate_data_against_schema(self, schema: Schema, input_data) -> bool:
        if schema.schema_type == 'AVRO':    
            fastavro_schema = fastavro.parse_schema(json.loads(schema.schema_str))
            return fastavro.validate(datum=input_data, schema=fastavro_schema)
        else:
            raise NotImplementedError(f"Schema type {schema.schema_type} is not implemented for validation. Use avro for now")