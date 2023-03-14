import pandas as pd
import argparse

parser = parser = argparse.ArgumentParser()
parser.add_argument("InputCSVPath", help="The path to the input csv file", type=str)
parser.add_argument("OutputCSVPath", help="The path to the output csv file", type=str)
args = parser.parse_args()

# Read csv
df = pd.read_csv(args.InputCSVPath)
# Apply filter
filtered_df = df[df.job == "Social worker"]
# save output csv
filtered_df.to_csv(args.OutputCSVPath)
