import json
from collections import defaultdict
import numpy as np  # Importing NumPy

# Function to read JSON data from a file
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to write JSON data to a file
def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Paths to your JSON files
file_paths = ['scored_fork_uses_bai.json', 'scored_fork_uses_lichun.json']

# Dictionary to hold aggregated scores
aggregated_scores = defaultdict(lambda: {'originality_score': [], 'elaboration_score': []})

# Read each file and aggregate scores
for path in file_paths:
    contents = read_json(path)
    for entry in contents:
        use = entry['use']
        try:
            originality_score = int(entry['originality_score'])
            elaboration_score = int(entry['elaboration_score']) if entry['elaboration_score'] != "" else 0
            aggregated_scores[use]['originality_score'].append(originality_score)
            aggregated_scores[use]['elaboration_score'].append(elaboration_score)
        except ValueError:
            pass  # Ignore entries with invalid scores

# Calculate averages and standard deviations using NumPy
averaged_results = []
all_originality_scores = []
all_elaboration_scores = []
for use, scores in aggregated_scores.items():
    originality_scores = np.array(scores['originality_score'])
    elaboration_scores = np.array(scores['elaboration_score'])

    all_originality_scores.extend(scores['originality_score'])
    all_elaboration_scores.extend(scores['elaboration_score'])
    
    avg_originality_score = np.mean(originality_scores)
    avg_elaboration_score = np.mean(elaboration_scores) if elaboration_scores.size > 0 else 0
    std_dev_originality = np.std(originality_scores, ddof=1)  # ddof=1 for sample standard deviation
    std_dev_elaboration = np.std(elaboration_scores, ddof=1) if elaboration_scores.size > 0 else 0

    averaged_results.append({
        'item': 'Fork',
        'use': use,
        'originality_score': avg_originality_score,
        'elaboration_score': avg_elaboration_score,
        'std_dev_originality_score': std_dev_originality,
        'std_dev_elaboration_score': std_dev_elaboration
    })
# Overall standard deviations
overall_std_dev_originality = np.std(np.array(all_originality_scores).astype(int), ddof=1)
overall_std_dev_elaboration = np.std(np.array(all_elaboration_scores).astype(int), ddof=1) if all_elaboration_scores else 0

# Write averaged results and standard deviations to a new file
output_file_path = 'averaged_results_with_std_dev_numpy_bai_lichun.json'
write_json(averaged_results, output_file_path)

print(f"Averaged scores and standard deviations (using NumPy) have been saved to {output_file_path}")
print(f"Overall standard deviation for originality: {overall_std_dev_originality:.2f}")
print(f"Overall standard deviation for elaboration: {overall_std_dev_elaboration:.2f}")
