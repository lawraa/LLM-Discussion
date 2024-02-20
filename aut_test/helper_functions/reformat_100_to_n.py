import json

input_file_name = '/home/phoebelu/AUT_test/Results/reproduce_result/utility/AUT_reproduce_utility_YES_1_01-24_22:03:58.json'  # Update with your input file path
output_file_name = '/home/phoebelu/AUT_test/Results/reproduce_result/utility/AUT_30_reproduce_utility_YES_1_01-24_22:03:58.json'  # Update with your desired output file path
aut_30_file_path = '/home/phoebelu/AUT_test/datasets/aut_30.json'
# Load the 'result' JSON data
with open(input_file_name) as file:
    result_data = json.load(file)

# Load the 'item list' JSON data
with open(aut_30_file_path) as file:
    item_list_data = json.load(file)

# Extract the list of objects from 'item list'
objects_in_item_list = [item["object"] for item in item_list_data["examples"]]

# Filter 'result' data
filtered_results = [item for item in result_data if item["item"] in objects_in_item_list]

# Optionally, write the filtered results to a new JSON file
with open(output_file_name, 'w') as outfile:
    json.dump(filtered_results, outfile, indent=4)

# If you just want to print the result
print(json.dumps(filtered_results, indent=4))
