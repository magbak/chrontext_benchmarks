import sqlalchemy as sa
import os
import pandas as pd
import pathlib

PATH_HERE = pathlib.Path(__file__).parent

engine = sa.create_engine('postgresql://postgresuser:secretPassword1234@postgres-0.postgres.otit.svc.cluster.local:5432/otit')

for f in os.listdir(PATH_HERE / "tables"):
    table_name = f.replace(".parquet", "")
    df = pd.read_parquet(PATH_HERE / "tables" / str(f))

    if table_name == "HTTPSGITHUBCOMMAGBAKCHRONTEXTSWTHASSTATICVALUE":
        object_datatype = "INT"
    else:
        object_datatype = "VARCHAR(255)"
    resp = df.to_sql(table_name, engine, index=False, if_exists="replace")
    create_subject_index = f"CREATE INDEX {table_name + '_sind'} ON {table_name} (subject)"
    engine.execute(create_subject_index)
    create_object_index = f"CREATE INDEX {table_name + '_oind'} ON {table_name} (subject)"
    engine.execute(create_object_index)
    print("DF ", table_name, df)
    print(resp)

