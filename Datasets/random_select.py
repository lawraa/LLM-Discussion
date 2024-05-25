import json
import random

# Original JSON data partially provided in the user's question
data_file_path = "Similarities/similarities_30_test.json"
task = "Similarities"
# Load the original data
with open(data_file_path, "r") as f:
    data = json.load(f)
if task == "AUT":
    # Select 30 random examples from the original data
    selected_examples = random.sample(data["Examples"], 30)

    # Update the "Examples" key with the selected examples and adjust the "Amount"
    new_data = {
        "Task": data["Task"],  # Assuming we want to keep the tasks unchanged
        "Examples": selected_examples,
        "Amount": 30
    }
elif task == "Instances" or task == "Similarities":
    selected_examples = random.sample(data["Examples"], 30)
    new_data = {
        "Examples": selected_examples,
        "Amount": 30
    }
elif task == "Scientific":
    selected_examples = []
    for task in data["Task"]:
        if len(task["Example"]) >= 6:  # Ensure there are at least 6 examples to choose from
            selected = random.sample(task["Example"], 6)  # Randomly select 6 examples
            selected_examples.append({
                "Original": task["Original"],
                "Example": selected,
                "Amount": "6"
            })

    # New data structure with selected examples for each task
    new_data = {
        "Task": selected_examples
    }

# Save the new data into a JSON file
new_file_path = 'selected_examples.json'

with open(new_file_path, 'w') as f:
    json.dump(new_data, f, indent=4)

new_file_path
