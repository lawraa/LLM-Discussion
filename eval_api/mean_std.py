import json
import numpy as np
import matplotlib.pyplot as plt
filename = "evaluation_Curr_classify_answers_50_3"
filepath = f'/home/chenlawrance/repo/LLM-Creativity/eval_api/result/{filename}.json'


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

scores_current, mean_std_current = calculate_mean_std(filepath)

# Print the mean and standard deviation
print(f"File: {filename}.json")
for category in mean_std_current:
    print(f"{category} - Mean: {mean_std_current[category]['mean']}, Standard Deviation: {mean_std_current[category]['std']}")

