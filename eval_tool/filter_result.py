import json
import os

def is_valid_fluency(response):
    required_keys = ["number_of_responses", "evaluation_explanation", "listed_responses"]
    return 'results' in response and all(key in response["results"] and response["results"][key] is not None for key in required_keys)

def is_valid_flexibility(response):
    required_keys = ["total_flexibility_score", "evaluation_explanation", "listed_categories"]
    return 'results' in response and all(key in response["results"] and response["results"][key] is not None for key in required_keys)

def is_valid_originality(response):
    required_keys = ["originality_rating", "evaluation_explanation"]
    return 'results' in response and all(key in response["results"] and response["results"][key] is not None for key in required_keys)

def is_valid_elaboration(response):
    required_keys = ["elaboration_rating", "evaluation_explanation"]
    return 'results' in response and all(key in response["results"] and response["results"][key] is not None for key in required_keys)


def filter_results(input_file):
    # Ensure the ./result/ directory exists
    result_dir = './result'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Load the JSON data from the output file
    with open(f'{result_dir}/{input_file}.json', 'r') as file:
        data = json.load(file)

    # Filter out invalid responses for each category
    for category in ["fluency", "flexibility", "originality", "elaboration"]:
        validation_function = globals()[f"is_valid_{category}"]
        for item in data[category]:
            item["responses"] = [response for response in item["responses"] if validation_function(response)]

    # Save the filtered data to a new JSON file
    filtered_output_file = f'{result_dir}/filtered_{input_file}.json'
    with open(filtered_output_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Filtered data has been saved to '{filtered_output_file}'")
    return f'filtered_{input_file}'

if __name__ == "__main__":
    filter_results("evaluation_phoebe_response_4")
