import json

# Load the JSON data
file_path = "/home/chenlawrance/exp_repo/LLM-Creativity/Results/AUT/Output/single_agent/AUT_single_single_brainstorm_baseline_1_1_gpt-35turbo-0125_None_final_03-25-06-13-53_10.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Process the data
transformed_data = []
for item in data:
    if item["type"] == "Yes":
        # Check if this item already exists in the transformed data
        existing_item = next((x for x in transformed_data if x["item"] == item["item"]), None)
        if existing_item:
            # If item exists, append the uses to the existing item's uses list
            existing_item["uses"].extend(item["uses"])
        else:
            # If not, add the item as is
            transformed_data.append(item)
    # If "No", do nothing (effectively filtering out)

# Save the transformed data back to a new JSON file
new_file_path = "/home/chenlawrance/exp_repo/LLM-Creativity/Results/AUT/Output/single_agent/AUT_single_single_brainstorm_baseline_1_1_gpt-35turbo-0125_None_final-yesfilter_03-25-06-13-53_10.json"
with open(new_file_path, 'w') as file:
    json.dump(transformed_data, file, indent=4)

new_file_path
