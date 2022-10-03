import great_expectations as ge
import pandas as pd
from urllib.request import urlopen

dataset = pd.read_csv("../test.csv")
print (f"{len(dataset)} rows")
dataset.head(5)

df = ge.dataset.PandasDataset(dataset)


df.expect_table_columns_to_match_ordered_list(
    column_list=["id","url_legal","license","excerpt","target","standard_error"]
)

df.expect_column_values_to_not_be_null(column="target")

df.expect_column_values_to_not_be_null(column="id")
df.expect_column_values_to_be_unique(column="id")

df.expect_column_values_to_not_be_null(column="excerpt")
df.expect_column_values_to_be_of_type(column="excerpt", type_="str")

# Expectation suite
expectation_suite = df.get_expectation_suite(discard_failed_expectations=False)
print(df.validate(expectation_suite=expectation_suite, only_return_failures=True))
