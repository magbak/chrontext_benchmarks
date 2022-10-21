import SPARQLWrapper

query = """
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    PREFIX ct:<https://github.com/magbak/chrontext#>
    PREFIX wp:<https://github.com/magbak/chrontext/windpower_example#>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rds:<https://github.com/magbak/chrontext/rds_power#>
    SELECT ?site ?wtur ?wtur_label ?dt  WHERE {
        ?site a rds:Site . 
        ?site rds:hasFunctionalAspect ?wtur_asp .
        ?wtur_asp rdfs:label ?wtur_label .
        ?wtur rds:hasFunctionalAspectNode ?wtur_asp .
        ?wtur ct:hasTimeseries ?ts .
        ?ts ct:hasDatatype ?dt .
        FILTER(?wtur_label = "A1") .
    }
"""
# query = """
#     PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
#     PREFIX ct:<https://github.com/magbak/chrontext#>
#     PREFIX wp:<https://github.com/magbak/chrontext/windpower_example#>
#     PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#     PREFIX rds:<https://github.com/magbak/chrontext/rds_power#>
#     SELECT ?site ?wtur ?wtur_label ?ts ?val ?t WHERE {
#         ?site a rds:Site .
#         ?site rds:hasFunctionalAspect ?wtur_asp .
#         ?wtur_asp rdfs:label ?wtur_label .
#         ?wtur rds:hasFunctionalAspectNode ?wtur_asp .
#         ?wtur rds:hasFunctionalAspect ?gensys_asp .
#         ?gensys rds:hasFunctionalAspectNode ?gensys_asp .
#         ?gensys ct:hasTimeseries ?ts .
#         ?ts ct:hasDataPoint ?dp .
#         ?dp ct:hasDataValue ?val .
#         ?dp ct:hasTimestamp ?t .
#         FILTER(?wtur_label = "A1") .
#     }
# """
wrp = SPARQLWrapper.SPARQLWrapper(endpoint="http://ontop.otit.svc.cluster.local:8080/sparql")
wrp.setQuery(query)
wrp.setReturnFormat(SPARQLWrapper.JSON)
res = wrp.query().convert()
print(res)
