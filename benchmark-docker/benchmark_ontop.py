import os
from time import time
import SPARQLWrapper
import sparql_dataframe

n = 12

times = []

endpoint = "http://ontop.otit.svc.cluster.local:8080/sparql"

for f in os.listdir("queries_ontop"):
    print("Query: " + f.replace(".sparql", ""))
    with open("queries_ontop/" + f) as qf:
        query = qf.read()

    firstiter = True
    for i in range(1, n + 1):
        print("Iteration " + str(i))
        if firstiter:
            print("First iteration, creating csv")
            try:
                df = sparql_dataframe.get(endpoint, query)
                df.to_csv(f"output/ontop_out_{f}_{i}.csv")
            except Exception as e:
                print("Error")
                print(str(e))
            firstiter = False

        else:
            try:
                wrp = SPARQLWrapper.SPARQLWrapper(endpoint=endpoint)
                wrp.setQuery(query)
                wrp.setReturnFormat(SPARQLWrapper.JSON)
                t = time()
                res = wrp.query().convert()
                took = time() - t
                times.append((f, i, took))
                print("Took " + str(took))
                if took > 600:
                    print("Took more than 600 seconds, aborting case")
                    break
            except Exception as e:
                print("Error!")
                print(str(e))
                times.append((f, i, "F"))
                break


print(times)
