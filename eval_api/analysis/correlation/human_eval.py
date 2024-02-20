import json
import random

# Load the JSON data from file
with open('fork_uses.json', 'r') as file:
    fork_uses = json.load(file)

# Shuffle the list to randomize the order
random.shuffle(fork_uses)

# Initialize a list to hold scored items
scored_items = []

# Iterate through the randomized list of fork uses
for item in fork_uses:
    print(f"Item: {item['item']}")
    for use in item['uses']:
        print(f"Use: {use}")
        
        # Get originality and elaboration scores from the user
        originality_score = input("Enter originality score (1-5): ")
        elaboration_score = input("Enter elaboration score (1-5): ")
        
        # Append scores and the use to the scored_items list
        scored_item = {
            "item": item["item"],
            "use": use,
            "originality_score": originality_score,
            "elaboration_score": elaboration_score
        }
        scored_items.append(scored_item)

        # Optional: Add a break if you want to test with just one iteration
        # break

# Save the scored items to a new JSON file
with open('scored_fork_uses.json', 'w') as outfile:
    json.dump(scored_items, outfile, indent=4)

print("All items have been scored and saved to 'scored_fork_uses.json'.")
