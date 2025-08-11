import duckdb

conn = duckdb.connect(database= '/Users/alisoncordoba/fir8aug/duckdbdump/lake.duckdb')

conn.execute("INSTALL 'ducklake'")
conn.execute("LOAD 'ducklake'")


conn.execute("ATTACH 'ducklake:/Users/alisoncordoba/fir8aug/duckdbdump/catalog.duckdb' AS my_lake (DATA_PATH '/Users/alisoncordoba/fir8aug/duckdbdump/data')")
conn.execute("USE my_lake")

conn.execute("CREATE TABLE IF NOT EXISTS penguins AS SELECT * FROM penguins.csv")

conn.close()