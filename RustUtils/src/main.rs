use polars::{prelude::*, lazy::dsl::col};
use std::env;

fn main() {
    // Setting arguments for input and output csv
    let args: Vec<String> = env::args().collect();
    let csv_path = &args[1];
    let result_path = &args[2];

    // Reading csv files into a polars dataframe
    let df = CsvReader::from_path(csv_path).unwrap().finish().unwrap();

    // use the predicate to filter
    let predicate = col("job").eq(lit("Social worker"));
   
    let filtered_df = df
                    .clone()
                    .lazy()
                    .filter(predicate )
                    .collect()
                    .unwrap();

    let mut output = filtered_df;
    
    // Writing to a csv file
    let mut file = std::fs::File::create(result_path).unwrap();
    CsvWriter::new(&mut file).finish(&mut output).unwrap();
}



// published file can be run using this command 
// Measure-Command{C:\Users\Navada\Documents\RustProjects\data_processer\target\release\data_processer.exe  "C:\Users\Navada\Documents\RustProjects\data_processer\input.csv"  "C:\Users\Navada\Documents\RustProjects\data_processer\output.csv"}