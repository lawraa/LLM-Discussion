import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

original_data = read_json('scientific_100.json')

# Function to determine category based on the test ID
def determine_category(test_id):
    categories = {
        "Test1": "Scientific Innovation",
        "Test2": "Hypothetical Scenarios",
        "Test3": "Product Improvement",
        "Test4": "Imaginative Physics",
        "Test5": "Comparative Analysis"
    }
    return categories.get(test_id, "General")

# Process the original data to create a simplified list
simplified_data = []
for test_id, test_info in original_data.items():
    category = determine_category(test_id)
    for question in test_info["example"]:
        simplified_data.append({
            "question": question,
            "category": category
        })

# Optionally, convert the simplified list to JSON format and print or save it
simplified_json = json.dumps(simplified_data, indent=4)
print(simplified_json)

# If you want to save the simplified data to a file
with open('processed_scientific_100.json', 'w') as file:
    file.write(simplified_json)
