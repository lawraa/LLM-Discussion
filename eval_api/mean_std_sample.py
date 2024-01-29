import json
import numpy as np

# Load the provided JSON file
file_path = './result_sample/evaluation_AUT_originality_NO_01-29_11:41:06_3_sample.json'
#file_path = './result_sample/evaluation_AUT_originality_YES_01-29_11:41:06_3_sample.json'  # Replace with your file path
#file_path = './result_sample/evaluation_AUT_originality_ALL_01-29_11:41:06_3_sample.json'
print("NO")
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract "average_originality" and "average_elaboration" values
average_originality = [item['average_originality'] for item in data if 'average_originality' in item]
average_elaboration = [item['average_elaboration'] for item in data if 'average_elaboration' in item]

# Calculate mean and standard deviation
mean_originality = np.mean(average_originality)
std_dev_originality = np.std(average_originality)

mean_elaboration = np.mean(average_elaboration)
std_dev_elaboration = np.std(average_elaboration)

# Print results
print("Average Originality - Mean:", mean_originality, ", Standard Deviation:", std_dev_originality)
print("Average Elaboration - Mean:", mean_elaboration, ", Standard Deviation:", std_dev_elaboration)
