print("Customer360 Databricks project")
print("Spark version:", spark.version)

df = (spark.range(10))

display(df)