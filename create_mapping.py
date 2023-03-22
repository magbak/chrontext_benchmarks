import rdflib
from rdflib import Graph, URIRef, Literal
import polars as pl
import pathlib

EXAMPLE_PREFIX = "https://github.com/magbak/chrontext/windpower_example#"
RDS_PREFIX = "https://github.com/magbak/chrontext/rds_power#"
XSD_PREFIX = "http://www.w3.org/2001/XMLSchema#"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
PATH_HERE = pathlib.Path(__file__).parent

def create_table_name(iri: str):
    name = ""
    for c in iri:
        if c.isalpha():
            name += c
    name = name.lower().replace("httpsgithubcommagbakchrontext", "").replace("httpwwwworgrdfschema", "").replace("httpwwwworgrdfsyntaxns", "")
    return name


def build_target(triples):
    (_, v, o) = triples[0]
    o_type = type(o)
    if o_type == URIRef:
        if str(v) == RDF_TYPE:
            o_mapping = "rds:{object}"
        elif str(v) == "https://github.com/magbak/chrontext#hasDatatype":
            o_mapping = "xsd:{object}"
        else:
            o_mapping = "ex:{object}"
    elif o_type == Literal:
        o_mapping = "{object}^^" + str(o.datatype).replace("http://www.w3.org/2001/XMLSchema#", "xsd:")
    else:
        assert False
    return "ex:{subject} <" + str(v) + "> " + o_mapping + " ."


def build_sql_query(table_name):
    return f'SELECT * from "postgres"."public"."{table_name}"'


g = Graph()
g.parse(PATH_HERE / "windpower.nt", format="nt")
triples_dict = {}

for e in g:
    if str(e[1]) not in triples_dict:
        triples_dict[str(e[1])] = []
    triples_dict[str(e[1])].append(e)

keys = [k for k in triples_dict]
keys.sort()

mapping = "[PrefixDeclaration]\n"
mapping += f"ex:\t\t{EXAMPLE_PREFIX}\n"
mapping += f"rds:\t{RDS_PREFIX}\n"
mapping += "\n"
mapping += "[MappingDeclaration] @collection [["


mapping += """	
mappingId	timeseriesdouble
target	    ex:{datapoint_id} <https://github.com/magbak/chrontext_benchmark#hasYear> {dir0}^^xsd:int . ex:{datapoint_id} <https://github.com/magbak/chrontext_benchmark#hasMonth> {dir1}^^xsd:int .ex:{datapoint_id} <https://github.com/magbak/chrontext_benchmark#hasDay> {dir2}^^xsd:int . ex:{dir3} <https://github.com/magbak/chrontext#hasDataPoint> ex:{datapoint_id}. ex:{datapoint_id} <https://github.com/magbak/chrontext#hasValue> {value}^^xsd:double;  <https://github.com/magbak/chrontext#hasTimestamp> {timestamp}^^xsd:dateTime . 
source		SELECT "dir0", "dir1", "dir2", "dir3", "datapoint_id", "timestamp", "value" from "s3"."chrontext-benchmark"."timeseries_double"

mappingId	timeseriesboolean
target	    ex:{datapoint_id} <https://github.com/magbak/chrontext_benchmark#hasYear> {dir0}^^xsd:int . ex:{datapoint_id} <https://github.com/magbak/chrontext_benchmark#hasMonth> {dir1}^^xsd:int .ex:{datapoint_id} <https://github.com/magbak/chrontext_benchmark#hasDay> {dir2}^^xsd:int . ex:{dir3} <https://github.com/magbak/chrontext#hasDataPoint> ex:{datapoint_id}. ex:{datapoint_id} <https://github.com/magbak/chrontext#hasValue> {value}^^xsd:boolean;  <https://github.com/magbak/chrontext#hasTimestamp> {timestamp}^^xsd:dateTime .
source		SELECT "dir0", "dir1", "dir2", "dir3", "datapoint_id", "timestamp", "value" from "s3"."chrontext-benchmark"."timeseries_boolean"

"""


for k in keys:
    table_name = create_table_name(k)
    target = build_target(triples_dict[k])
    query = build_sql_query(table_name)

    mapping += f"mappingId\t{table_name}\n"
    mapping += f"target\t\t{target}\n"
    mapping += f"source\t\t{query}\n"
    mapping += "\n"

mapping += "]]"

with open("ontop-docker/mapping.obda", "w") as f:
    f.write(mapping)

for k in keys:
    subjects = []
    objects = []
    table_name = create_table_name(k)
    for (s, _, o) in triples_dict[k]:
        s_str = str(s).replace(EXAMPLE_PREFIX, "")
        o_type = type(o)
        if o_type == URIRef:
            o_rep = str(o).replace(EXAMPLE_PREFIX, "").replace(RDS_PREFIX, "").replace(XSD_PREFIX, "")
        elif o_type == Literal:
            if o.datatype == rdflib.XSD.string:
                o_rep = str(o.value)
            elif o.datatype == rdflib.XSD.long:
                o_rep = int(o.value)
            else:
                assert False

        subjects.append(s_str)
        objects.append(o_rep)

    df = pl.DataFrame({"object": objects, "subject": subjects})
    df.write_parquet((PATH_HERE / "benchmark-docker" / "tables" / f"{table_name}.parquet").absolute())
