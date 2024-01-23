import argparse
from filter_result import filter_results
from restructure_result import restructure_results

def main(input_file):
    filtered_file = filter_results(input_file)
    restructured_file = restructure_results(filtered_file)
    print(f"Process completed. Final output: '{restructured_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process evaluation results.')
    parser.add_argument('input_file', help='The input file name (without .json extension)')
    args = parser.parse_args()
    
    main(args.input_file)
