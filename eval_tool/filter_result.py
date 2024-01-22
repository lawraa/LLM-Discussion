import json
input_file = "evaluation_results_version_4"
# Load the JSON data from the output file
with open(f'{input_file}.json', 'r') as file:
    data = json.load(file)

# Function to check if a fluency response is valid
def is_valid_fluency(response):
    required_keys = ["total_fluency_score", "evaluation_explanation", "listed_responses"]
    return all(key in response["results"] and response["results"][key] is not None for key in required_keys)

# Function to check if a flexibility response is valid
def is_valid_flexibility(response):
    required_keys = ["total_flexibility_score", "evaluation_explanation", "listed_categories"]
    return all(key in response["results"] and response["results"][key] is not None for key in required_keys)

# Function to check if an originality response is valid
def is_valid_originality(response):
    required_keys = ["originality_rating", "evaluation_explanation"]
    return all(key in response["results"] and response["results"][key] is not None for key in required_keys)

# Function to check if an elaboration response is valid
def is_valid_elaboration(response):
    required_keys = ["elaboration_rating", "evaluation_explanation"]
    return all(key in response["results"] and response["results"][key] is not None for key in required_keys)

# Filter out invalid responses for each category
for category in ["fluency", "flexibility", "originality", "elaboration"]:
    validation_function = globals()[f"is_valid_{category}"]
    for item in data[category]:
        item["responses"] = [response for response in item["responses"] if validation_function(response)]

# Save the filtered data to a new JSON file
with open(f'filtered_{input_file}.json', 'w') as file:
    json.dump(data, file, indent=4)

print(f"Filtered data has been saved to 'filtered_{input_file}.json'")
