import json
import argparse
import os

# Set up argument parser
parser = argparse.ArgumentParser(description='Process some data.')
parser.add_argument('input_file_path', type=str, help='Path to the input file')
parser.add_argument('output_file_name', type=str, help='Name of the output file')
parser.add_argument('-o', '--other', action='store_true', help='Include entries of type Other')
parser.add_argument('-y', '--yes', action='store_true', help='Include entries of type Yes')
parser.add_argument('-n', '--no', action='store_true', help='Include entries of type No')

args = parser.parse_args()

# Check if at least one of the options is provided
if not (args.other or args.yes or args.no):
    parser.error("Please provide at least one of the entry types: -o, -y, -n")

# Extract directory of input file and construct output file path
input_dir = os.path.dirname(args.input_file_path)
output_file_path = os.path.join(input_dir, args.output_file_name)

# Load the JSON data
with open(args.input_file_path, 'r') as file:
    data = json.load(file)

# Process the data based on command line options
processed_data = {}
for entry in data:
    include_entry = False
    if args.other and entry['type'] == 'Other':
        include_entry = True
    if args.yes and entry['type'] == 'Yes':
        include_entry = True
    if args.no and entry['type'] == 'No':
        include_entry = True
    
    if include_entry:
        item = entry['item']
        if item not in processed_data:
            processed_data[item] = []
        processed_data[item].append(entry['uses'])

# Convert to desired format
formatted_data = [{"item": item, "uses": uses} for item, uses in processed_data.items()]

# Write to the specified output JSON file
with open(output_file_path, 'w') as outfile:
    json.dump(formatted_data, outfile, indent=4)
