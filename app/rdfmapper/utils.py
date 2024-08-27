# import re
# import uuid
# from pathlib import Path
# from functools import lru_cache

# from rdflib import Graph, URIRef, Literal, BNode, Namespace
# from rdflib.namespace import SKOS, RDF, DC, RDFS, OWL, XSD
# from rdflib.plugins.sparql.processor import SPARQLResult

# import logging
# logging.basicConfig(level=logging.DEBUG)
# # utils_log = logging.getLogger('rutils_log')

# import logging
# rmap_log = logging.getLogger('rmap_log')


# # @lru_cache
# async def check_node_existence(graph, rdftype, rdfslabel, named_graph_identifier): # -> URIRef:
#     """Leibniz : Deux noeuds égaux sont deux noeuds ayant les mêmes propriétés.
#     Des questions sur l'isomorphisme de deux graphes partiels aussi.
#     QuickAndDirty -> Implanté ici, deux noeuds sont égaux si ils ont le même rdf:label
#     Returns:
#         URIRef: l'URI du noeud ayant le même type et le même label, None sinon
#     """
    
#     q_default = """ PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#> 
#         SELECT ?s 
#         WHERE {{
#             ?s a <{rdftype}> .
#             ?s rdfs:label "{rdfslabel}"
#         }}""".format(rdftype=rdftype,rdfslabel=rdfslabel)

#     q = """SELECT ?s 
#         FROM NAMED <{named_graph_identifier}>
#         WHERE {{
#             GRAPH ?g {{
#                 ?s a <{rdftype}> .
#                 ?s rdfs:label "{rdfslabel}"
#             }}
#         }}""".format(named_graph_identifier=named_graph_identifier, rdftype=rdftype, rdfslabel=rdfslabel)

#     r = graph.query(q)
#     if len(r.bindings) == 0:
#         logging.info(f"No existing node: '{rdfslabel}' typed <{rdftype}>")
#         return None
#     elif len(r.bindings) == 1:
#         existing_uri_node = URIRef(list(r.bindings[0].values())[0])
#         logging.info(f"Node already exists: <{existing_uri_node}> '{rdfslabel}' typed <{rdftype}>")
#         return existing_uri_node
#     else:
#         logging.warning(f"Duplicates! {len(r.bindings)} corresponding nodes found for '{rdfslabel}' typed <{rdftype}>. Retrieving the URI of the first one")
#         return URIRef(list(r.bindings[0].values())[0])


# async def create_node_and_label(graph, uri_root, named_graph_identifier, rdftype, rdfslabel, check_existence=False) -> URIRef:
#     def uri_maker_as_type_uuid() -> URIRef:
#         uri_name = re.search('([^\/]+?(?=_))', Path(rdftype).stem)[0] + '-' + str(uuid.uuid4())[:8]
#         return URIRef(uri_root + uri_name)

#     my_uri =  None
#     if check_existence == True:
#         my_uri = await check_node_existence(graph, rdftype, rdfslabel, named_graph_identifier)
    
#     if my_uri == None:
#         my_uri = uri_maker_as_type_uuid()
#         logging.info(f"CREATING node '{rdfslabel}' at uri <{str(my_uri)}>")
#     else:
#         logging.info(f"Node already exists in graph <{named_graph_identifier}>")
#         return my_uri
    
#     graph.add((my_uri, RDF.type, rdftype))
#     graph.add((my_uri, RDFS.label, Literal(rdfslabel)))

#     return my_uri