import json
import numpy as np
import matplotlib.pyplot as plt

file_path_current = '/home/chenlawrance/repo/LLM-Creativity/eval_api/result/evaluation_Curr_classify_answers_50_3.json'
file_path_previous = '/home/chenlawrance/repo/LLM-Creativity/eval_api/result/evaluation_Prev_classify_answers_50_3.json'

def calculate_mean_std(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    scores = {"fluency": [], "flexibility": [], "originality": [], "elaboration": []}
    for item in data:
        for category in scores.keys():
            if category in item:
                scores[category].append(item[category]["average_score"])
    print("fluency score: ", scores["fluency"])
    print("flexibility score: ", scores["flexibility"])
    print("originality score: ", scores["originality"])
    print("elaboration score: ", scores["elaboration"])
    mean_std = {category: {"mean": np.mean(scores[category]), "std": np.std(scores[category])} for category in scores}
    return scores, mean_std

# Calculate for current and previous files
print("CURRENT -------------------")
scores_current, mean_std_current = calculate_mean_std(file_path_current)
print("PREVIOUS -------------------")
scores_previous, mean_std_previous = calculate_mean_std(file_path_previous)

# Plotting the graphs
categories = ["fluency", "flexibility", "originality", "elaboration"]
for category in categories:
    plt.figure()
    
    # Current scores
    current_scores = scores_current[category]
    plt.scatter(range(len(current_scores)), current_scores, facecolors='none', edgecolors='b', marker='o', label='Current')

    # Previous scores - Red 'x'
    previous_scores = scores_previous[category]
    plt.scatter(range(len(previous_scores)), previous_scores, color='r', marker='x', label='Previous')

    plt.title(f"{category.capitalize()} Scores")
    plt.xlabel('Sample')
    plt.ylabel('Score')
    plt.legend()
    plt.savefig(f"{category}_scores.png") 

# Print the mean and standard deviation
print("Current File:")
for category in mean_std_current:
    print(f"{category} - Mean: {mean_std_current[category]['mean']}, Standard Deviation: {mean_std_current[category]['std']}")

print("\nPrevious File:")
for category in mean_std_previous:
    print(f"{category} - Mean: {mean_std_previous[category]['mean']}, Standard Deviation: {mean_std_previous[category]['std']}")
