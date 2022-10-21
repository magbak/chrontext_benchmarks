import sqlalchemy as sa
import pandas as pd
import os
import pathlib

PATH_HERE = pathlib.Path(__file__).parent

engine = sa.create_engine('postgresql://postgresuser:secretPassword1234@postgres-0.postgres.otit.svc.cluster.local:5432/otit')

for f in os.listdir(PATH_HERE / "tables"):
    table_name = f.replace(".parquet", "")
    print(table_name)
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    print(df)
