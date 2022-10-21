from chrontext import Engine, ArrowFlightSQLDatabase, TimeSeriesTable
import polars as pl

ENDPOINT ="http://ontop.otit.svc.cluster.local:8080/sparql"

engine = Engine(ENDPOINT)
tables = [
    TimeSeriesTable(
        schema="s3",
        time_series_table="otit-benchmark.timeseries_double",
        value_column="value",
        timestamp_column="timestamp",
        identifier_column="dir3",
        value_datatype="http://www.w3.org/2001/XMLSchema#double",
        year_column="dir0",
        month_column="dir1",
        day_column="dir2"),
    TimeSeriesTable(
        schema="s3",
        time_series_table="otit-benchmark.timeseries_boolean",
        value_column="value",
        timestamp_column="timestamp",
        identifier_column="dir3",
        value_datatype="http://www.w3.org/2001/XMLSchema#boolean",
        year_column="dir0",
        month_column="dir1",
        day_column="dir2")
]
arrow_flight_sql_database = ArrowFlightSQLDatabase(host="dremio.otit.svc.cluster.local", port=32010, username="dremio",
                                                   password="dremio123", tables=tables)
engine.set_arrow_flight_sql(arrow_flight_sql_database)
df = engine.execute_hybrid_query("""
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    PREFIX ct:<https://github.com/magbak/chrontext#>
    PREFIX wp:<https://github.com/magbak/chrontext/windpower_example#>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rds:<https://github.com/magbak/chrontext/rds_power#>
    SELECT ?site ?wtur ?wtur_label ?ts ?val ?t WHERE {
        ?site a rds:Site . 
        ?site rds:hasFunctionalAspect ?wtur_asp .
        ?wtur_asp rdfs:label ?wtur_label .
        ?wtur rds:hasFunctionalAspectNode ?wtur_asp .
        ?wtur rds:hasFunctionalAspect ?gensys_asp .
        ?gensys rds:hasFunctionalAspectNode ?gensys_asp .
        ?gensys ct:hasTimeseries ?ts .
        ?ts ct:hasDataPoint ?dp . 
        ?dp ct:hasValue ?val .
        ?dp ct:hasTimestamp ?t .
        FILTER(?wtur_label = "A1" && ?t > "2022-06-01T08:46:53"^^xsd:dateTime) .
    }
""")

print(df)