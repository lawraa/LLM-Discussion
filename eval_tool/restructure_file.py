import json

input_file = "filtered_evaluation_results_version_4"
# Load the JSON data from the output file
with open(f'{input_file}.json', 'r') as file:
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

# # Save the combined data to a new JSON file
# with open('combined_output_file.json', 'w') as file:
#     json.dump({'items': combined_data}, file, indent=4)

# print("Combined data has been saved to 'combined_output_file.json'")

# Save the restructured data to a new JSON file
with open(f'restructured_{input_file}.json', 'w') as file:
    json.dump(combined_data, file, indent=4)

print(f"Filtered data has been saved to 'restructured_{input_file}.json'")



