import os
import re
import uuid
from string import Template
from pathlib import Path

from typing import Mapping, Union, Any

from app.main import app
from app.schemaregistry_basicapi import InlkSchemaRClient

# from app.rdfmapper.rdfmapper import map_to_rdf
from rdflib.plugins.stores import sparqlstore
from urllib.parse import urlparse
from urllib.error import URLError

from app.rdfmapper.fast_triplestore import TripleStore


import logging

g_logger = logging.getLogger("g_log")

in_topic = app.topic("inlake-gateway")
# uentries_topic = app.topic("streamgraphiti-unprocessable-entries")
sgjobs_topic = app.topic("jobs-streamgraphiti")

# CODE_DIR = Path(__file__).resolve().parents[2]
# TEMPLATE_DIR = Path(CODE_DIR, "sparql_templates")
# TEST_PATH_TEMPLATE_FOAF = Path(
#     TEMPLATE_DIR, "rdfgraph-graphdb_update_template-foaf_person.sparql"
# )


def kkey_to_parameters(kkey: str):
    o = urlparse(kkey)
    return o.scheme, o.netloc, o.path.lstrip("/")


triplestore = TripleStore(
    config_store={
        "query_endpoint": os.environ["SPARQL_ENDPOINT_QUERY"],
        "update_endpoint": os.environ["SPARQL_ENDPOINT_UPDATE"],
    },
    config={
        "default_triples_root_uri": os.environ["SPARQL_DEFAULT_ROOT_URI"],
        "default_named_graph_root_uri": os.environ[
            "SPARQL_DEFAULT_NAMED_GRAPH_ROOT_URI"
        ],
        "default_named_graph_name": os.environ["SPARQL_DEFAULT_NAMED_GRAPH_NAME"],
        "datapip_sparql_update_path": "/data/sparql-update",  # Load `/data/sparql-select` directory with DockerFile or Compose File
    },
)


@app.agent(in_topic)
async def agent_mapper(stream):
    async for key, v in stream.items():
        kkey = key.decode("utf-8")
        duuid, key_schema, graph_destination_override = kkey_to_parameters(kkey)
        
        # # Checking schema existence
        # client_schema = InlkSchemaRClient()
        # await client_schema.connect_sr({"url": os.environ['SCHEMA_REGISTRY_URL']})
        # if client_schema.check_existence(key_schema) is False:
        #     # UNPROCESSABLE Sending message to "unprocessable entries" topic.
        #     # TODO: apply strategy to reprocess messages later with the "app.unprocessable_entries" agent
        #     logging.warning(f"schema={key_schema} not found on Schema Registry, message pending for 7days at {uentries_topic.topics}")
        #     await uentries_topic.send(key=key, value=v, value_serializer=None, key_serializer=None)
        # elif key_schema not in [mapper for mapper in dict_schema_mapper]:
        #     logging.warning(f"schema={key_schema} does not have an attributed mapper in this StreamGraphiti instance, message pending for 7days at {uentries_topic.topics}")
        #     await uentries_topic.send(key=key, value=v, value_serializer=None, key_serializer=None)
        logging.info(
            f"Received msg keyed : duuid={duuid} key_schema={key_schema} with graph_destination_override={graph_destination_override}"
        )

        # else:
        # PROCESS TO RDF
        await sgjobs_topic.send(
            key=f"{duuid}://start",
            value={"template": key_schema},
            value_serializer=None,
            key_serializer=None,
        )

        query_filename = str(key_schema + ".sparql")
        query_graph_uri = f"{triplestore.config['default_named_graph_root_uri']}{graph_destination_override}" if (graph_destination_override != '') else triplestore.config['default_named_graph_name']

        if (graph_destination_override != ''):
            query_graph_uri = f"{triplestore.config['default_named_graph_root_uri']}{graph_destination_override}"
        else:
            query_graph_uri = f"{triplestore.config['default_named_graph_root_uri']}{triplestore.config['default_named_graph_name']}"

        logging.info(
            f"{duuid} PROCESSING to 3S endpoint={triplestore.config_store['update_endpoint']} to query_graph_uri={query_graph_uri}"
        )
        # JOB
        
        logging.info(f"values={v}")
        r = triplestore.update_templated(
            query_filename=query_filename,  # "u7cc3-dscrs.sparql",
            query_graph_override=query_graph_uri,
            **v,
        )



        if isinstance(r, Exception):
            logging.error(f"{duuid} FAILED")
            await sgjobs_topic.send(
                key=f"{duuid}://end",
                value={"status": "error", 
                       "e": f"{type(r)}-{r}"},
                value_serializer=None,
                key_serializer=None,
            )
        else:
            logging.info(f"{duuid} SUCCESS")
            await sgjobs_topic.send(
                key=f"{duuid}://end",
                value={"status": "success",
                       "uris": r},
                # uris={r}
                value_serializer=None,
                key_serializer=None,
            )




# async def context_processor_sparqlstore_update(
#     sparqlstore: sparqlstore.SPARQLUpdateStore,
#     named_graph: str,
#     uri_root: str,
#     path_queryfile: Path,
#     **kwargs,
# ):  # -> Union[Mapping[str, Any], Exception]
#     """Update an rdflib.Graph with a templated sparql query registered in a file.
#         Template specfications:
#             `$...` symbolizes a placeholder for a value to be substitued. Pay attention to sparql spectification such as `""` for literals and `<>` for uri definitions
#             `$__uri__...` uses an uri builder. The one in use is `simple_uuid_uri_generator()`
#         More documentation built at: https://git-xen.lmgc.univ-montp2.fr/gros/astragale-astragale
#         Direct inheritance of this functiion from StreamGraphiti's own context processor: https://git-xen.lmgc.univ-montp2.fr/gros/astragale-streamgraphiti


#     Args:
#         sparqlstore (sparqlstore.SPARQLUpdateStore): _description_
#         named_graph (str): _description_
#         uri_root (str): the root uri of the triples to be produced by the update query (prefixing the generated uris)
#         path_queryfile (Path): path to the .sparql template file

#     Returns:
#         _type_: _description_
#     """
#     try:
#         with open(path_queryfile, "r", encoding="utf-8") as file:
#             s = file.read()
#             uris = {}
#             uris_match = set(
#                 re.findall(pattern="<\$__uri__(.*?)>", string=s)
#             )  # set(findall(pattern, string)) for distincts matches
#             for u_number in uris_match:

#                 def simple_uuid_uri_generator() -> str:
#                     return uri_root + str(uuid.uuid4())[:8]

#                 urikey = f"__uri__{u_number}"
#                 uris[urikey] = simple_uuid_uri_generator()
#             logging.debug(f"Created {len(uris_match)} URIs : {uris}")

#             supdate = Template(s).substitute(kwargs | uris)
#             logging.debug(f"--- --- SUBSTITUED TEMPLATE CONTENT --- ---\n{supdate}")
#             sparqlstore.update(supdate, queryGraph=named_graph)

#     except KeyError as ke:
#         logging.error(
#             f"Textual JSON data and specified SPARQL ingest schema does not match (context_processor_sparqlstore_update)"
#         )
#         logging.error(
#             f"Please, chech missing value \n {Template(s).safe_substitute(kwargs|uris)}"
#         )
#         return ke
#     except FileNotFoundError as fnfe:
#         logging.error(fnfe)
#         logging.error(f"No SPARQL file found at path : {path_queryfile}")
#         return fnfe
#     except URLError as ue:
#         logging.error(ue)
#         logging.error(
#             f"3S Error, check connection OR 3S Internal Error, check logs (especially the endpoint logs, query can be malformed with a falsy .sparql)"
#         )
#         return ue
#     except Exception as e:
#         logging.error(e)
#         logging.error(f"Unhandlede exception {e}")
#         return e
#     return uris
