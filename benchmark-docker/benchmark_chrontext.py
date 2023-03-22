import os
from time import time

from chrontext import Engine, ArrowFlightSQLDatabase, TimeSeriesTable

ENDPOINT = "http://ontop.chrontext.svc.cluster.local:8080/sparql"

engine = Engine(ENDPOINT)
tables = [
    TimeSeriesTable(
        schema="s3.otit-benchmark",
        time_series_table="timeseries_double",
        value_column="value",
        timestamp_column="timestamp",
        identifier_column="dir3",
        value_datatype="http://www.w3.org/2001/XMLSchema#double",
        year_column="dir0",
        month_column="dir1",
        day_column="dir2"),
    TimeSeriesTable(
        schema="s3.otit-benchmark",
        time_series_table="timeseries_boolean",
        value_column="value",
        timestamp_column="timestamp",
        identifier_column="dir3",
        value_datatype="http://www.w3.org/2001/XMLSchema#boolean",
        year_column="dir0",
        month_column="dir1",
        day_column="dir2")
]
arrow_flight_sql_database = ArrowFlightSQLDatabase(host="dremio-client.default.svc.cluster.local", port=32010,
                                                   username="mba",
                                                   password="Qi3CQzuqK5DTJcS", tables=tables)
engine.set_arrow_flight_sql(arrow_flight_sql_database)
n = 12
times = []
for f in os.listdir("queries_chrontext"):
    print("Query: " + f.replace(".sparql", ""))
    with open("queries_chrontext/" + f) as qf:
        query = qf.read()
    firstiter = True
    for i in range(1, n + 1):
        print("Iteration " + str(i))
        try:
            t = time()
            df = engine.execute_hybrid_query(query)
            took = time() - t
            times.append((f, i, took))
            print("Took " + str(took))
            print(df)
            if firstiter:
                df.write_csv(f"output/chrontext_out_{f}_{i}.csv")
                firstiter = False
            if took > 600:
                print("Took more than 600 seconds, aborting case")
                break
        except Exception as e:
            print("Error!")
            print(str(e))
            times.append((f, i, "F"))
            break


print(times)
