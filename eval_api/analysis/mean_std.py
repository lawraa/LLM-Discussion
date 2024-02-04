import json
import numpy as np
import argparse
import os

def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON in the file: {file_path}")
        exit(1)

def mean_std_sample(data):
    originality = [item['average_originality'] for item in data if 'average_originality' in item]
    elaboration = [item['average_elaboration'] for item in data if 'average_elaboration' in item]

    return np.mean(originality), np.std(originality), np.mean(elaboration), np.std(elaboration)

def mean_std(data):
    scores = {"fluency": [], "flexibility": [], "originality": [], "elaboration": []}
    for item in data:
        for category in scores:
            if category in item:
                scores[category].append(item[category]["average_score"])

    return {category: {"mean": np.mean(scores[category]), "std": np.std(scores[category])} for category in scores}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find mean and standard deviation of sample JSON files")
    parser.add_argument("--input_file_path", required=True, help="File path of the JSON file")
    parser.add_argument("--type", choices=['default', 'sample'], default='default', help="Type of evaluation")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file_path):
        print(f"File does not exist: {args.input_file_path}")
        exit(1)

    data = read_json_file(args.input_file_path)

    if args.type == "sample":
        mean_originality, std_originality, mean_elaboration, std_elaboration = mean_std_sample(data)
        print(f"File: {args.input_file_path}\n"
              f"Average Originality - Mean: {mean_originality}, Standard Deviation: {std_originality}\n"
              f"Average Elaboration - Mean: {mean_elaboration}, Standard Deviation: {std_elaboration}")

    elif args.type == "default":
        mean_std_results = mean_std(data)
        print(f"File: {args.input_file_path}")
        for category, stats in mean_std_results.items():
            print(f"{category.capitalize()} - Mean: {stats['mean']}, Standard Deviation: {stats['std']}")
