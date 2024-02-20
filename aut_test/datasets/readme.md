# AUT - Alternative Use Test


## Run Experiments
In folder `run_exp`, you can find different frameworks of experiments on AUT.
### Reproduce "Brainstorm then Select"
`cd  reproduce`
#### Utility Test
`python reproduce_utility.py`
the output result is in `aut_test/results/reproduce/utility_result`
#### Originality Test
`python reproduce_originality.py`
the output result is in `aut_test/results/reproduce/originality_result`
#### Filter
To Extract answers with "YES/NO/OTHER", please check the usage of `answer_filter.py` below.
##### answer_filter.py
To use `answer_filter.py`, you must specify the input file path, the output file name, and at least one of the entry types to filter by. The command-line options for entry types are `-o` (Other), `-y` (Yes), and `-n` (No).

###### Command-Line Arguments
- `input_file_path`: The full path to the input JSON file.
- `output_file_name`: The name of the output JSON file. The output file will be saved in the same directory as the input file.
- `-o` or `--other`: Include entries of type `Other`.
- `-y` or `--yes`: Include entries of type `Yes`.
- `-n` or `--no`: Include entries of type `No`.

###### Examples
1. To filter entries of type `Other` from `input.json` and write to `output.json`:
`python answer_filter.py input_path/input.json output.json -o`

2. To filter entries of type `Yes` and `No` from `input.json`:
`python answer_filter.py input_path/input.json output.json -y -n`


###### Notes

- Ensure that you have the necessary permissions to read the input file and write to the output directory.
- The script will overwrite the output file if it already exists.



## Reformmating Outputs