import json

def restructure_results(input_file):
    # Load the JSON data from the output file
    input_path = f'./result/{input_file}.json'
    with open(input_path, 'r') as file:
        data = json.load(file)

    # Combine the data into a new structure
    combined_data = []
    for fluency, flexibility, originality, elaboration in zip(data['fluency'], data['flexibility'], data['originality'], data['elaboration']):
        # Assuming 'item' and 'result' are the same across all categories for each entry
        item = fluency['item']
        result = fluency['result']
        combined_entry = {
            'item': item,
            'result': result,
            'fluency': {
                'average_score': fluency['average_score'],
                'responses': fluency['responses']
            },
            'flexibility': {
                'average_score': flexibility['average_score'],
                'responses': flexibility['responses']
            },
            'originality': {
                'average_score': originality['average_score'],
                'responses': originality['responses']
            },
            'elaboration': {
                'average_score': elaboration['average_score'],
                'responses': elaboration['responses']
            }
        }
        combined_data.append(combined_entry)

    # Save the restructured data to a new JSON file
    restructured_output_file = f'./result/restructured_{input_file}.json'
    with open(restructured_output_file, 'w') as file:
        json.dump(combined_data, file, indent=4)

    print(f"Restructured data has been saved to '{restructured_output_file}'")
    return restructured_output_file

# The following part allows the script to be run independently
if __name__ == "__main__":
    restructure_results("filtered_evaluation_results_version_4")
