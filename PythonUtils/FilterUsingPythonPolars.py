import polars as pl
import argparse

parser = parser = argparse.ArgumentParser()
parser.add_argument("InputCSVPath", help="The path to the input csv file", type=str)
parser.add_argument("OutputCSVPath", help="The path to the output csv file", type=str)
args = parser.parse_args()

# Read csv
df = pl.read_csv(file=args.InputCSVPath) 
# Apply filter
filtered_df = df.filter(pl.col("job").str.contains("Social worker"))
# save output csv
filtered_df.write_csv(file=args.OutputCSVPath)
