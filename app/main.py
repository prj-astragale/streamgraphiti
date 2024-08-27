import os
import asyncio
from pathlib import Path
from logging.config import dictConfig
import configparser

import faust
from confluent_kafka.admin import AdminClient
from confluent_kafka import KafkaError, KafkaException

import logging
logging.basicConfig(level=logging.INFO)


logging_config = dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"default": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}},
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "loggers": {
            "g_log": {"handlers": ["console"], "level": "INFO"},
            "rmap_log": {"handlers": ["console"], "level": "INFO"}
            },
    })





try:
    # TODO: Defaulting variables for local environnment config
    logging.info(f"ENVIRONVAR {os.environ}")
except IOError:
    logging.warning(f"No environment variables defined, starting with defaulted values for local debugging session")
    
    from dotenv import load_dotenv
    load_dotenv()

    logging.warning(f"ENVIRONVAR {os.environ}")

app = faust.App(
    id='streamgraphiti',
    # id=1,
    # debug=global_config['core-config']['app.debug'],
    debug=True,
    autodiscover=["app.rdfmapper","app.unprocessable_entries"],
    broker=os.environ['KAFKA_BOOTSTRAP_SERVER'],
    store="memory://",
    logging_config=logging_config,
    # topic_allow_declare=settings.TOPIC_ALLOW_DECLARE,
    # topic_disable_leader=settings.TOPIC_DISABLE_LEADER,
    # broker_credentials=settings.SSL_CONTEXT,
)



### https://github.com/confluentinc/librdkafka/wiki/FAQ#i-want-to-get-an-event-when-brokers-come-up-and-down

# def retry(times, exceptions):
#     """
#     Retry Decorator
#     Retries the wrapped function/method `times` times if the exceptions listed
#     in ``exceptions`` are thrown
#     :param times: The number of times to repeat the wrapped function/method
#     :type times: Int
#     :param Exceptions: Lists of exceptions that trigger a retry attempt
#     :type Exceptions: Tuple of Exceptions
#     """
#     def decorator(func):
#         def newfn(*args, **kwargs):
#             attempt = 0
#             while attempt < times:
#                 try:
#                     return func(*args, **kwargs)
#                 except exceptions:
#                     print(
#                         'Exception thrown when attempting to run %s, attempt '
#                         '%d of %d' % (func, attempt, times)
#                     )
#                     attempt += 1
#             return func(*args, **kwargs)
#         return newfn
#     return decorator


# @app.on_before_configured.connect
# def on_startup_before_configuration(app, **kwargs):
#     # client = AdminClient({"bootstrap.servers": os.environ['KAFKA_BOOTSTRAP_SERVER']})
#     # client = AdminClient({"bootstrap.servers": 'brouker:80'})
    
#     # @retry(times=2, exceptions=(KafkaError, RuntimeError, KafkaException, Exception))
#     def get_kafka_client():
#         try:
#             logging.info(f"Connection attempt to broker {os.environ['KAFKA_BOOTSTRAP_SERVER']}")
#             client = AdminClient({"bootstrap.servers": 'brouker:80', 'error_cb': my_cb})
#             client.list_topics()
#         except (KafkaError, RuntimeError, KafkaException, Exception) as e:
#             logging.error(f'Error publishing to kafka : {e}')
#             return False
#         return True

#     if get_kafka_client():
#         logging.info("SGGGGGGGGGGGGGGGGG starting up")
#     else:
#         logging.critical(f"Error connecting to to broker {os.environ['KAFKA_BOOTSTRAP_SERVER']} after 3 attempts. Shutting down")

   
    # for i in range(3):
    #     logging.info(f"Connection attempt {i+1}/{3} to broker {os.environ['KAFKA_BOOTSTRAP_SERVER']}")
    #     try:
    #         client = AdminClient({"bootstrap.servers": 'brouker:80'})
    #     except:
    #         logging.error(f"Connection attempt {i+1}/{3}, retrying")
    
    # logging.critical(f"No broker available at {os.environ['KAFKA_BOOTSTRAP_SERVER']} after 3 attemps, shutting down")



if __name__ == '__main__':
    app.main()