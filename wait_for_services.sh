#!/bin/bash
set -e

cmd="$@"

# Connection check
## KAFKA
# until nc -vz ${KAFKA_BOOSTRAP_SERVER_NAME} ${KAFKA_BOOSTRAP_SERVER_PORT}; do
#   >&2 echo "Waiting for Kafka to be ready... - sleeping"
#   sleep 2
# done

# >&2 echo "(1/3) Kafka is up"

## SCHEMA REGISTRY
# until nc -vz ${SCHEMA_REGISTRY_SERVER} ${SCHEMA_REGISTRY_SERVER_PORT}; do
#   >&2 echo "Waiting for Schema Registry to be ready... - sleeping"
#   sleep 2
# done

# >&2 echo "(2/3) Schema Registry is up - executing command"

## TRIPLESTORE
# until nc -vz ${SPARQL_SERVER_NAME} ${SPARQL_SERVER_PORT}; do
#   >&2 echo "Waiting for Triple Store to be ready... - sleeping"
#   sleep 2
# done

# >&2 echo "(3/3) Triple store is up - executing command"
echo "Empty wait_for_services.sh, running the app without healtcheck"
echo "Executing command ${cmd}"
exec $cmd