import json
import numpy as np
import matplotlib.pyplot as plt

def calculate_mean_std(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    scores = {"fluency": [], "flexibility": [], "originality": [], "elaboration": []}
    for item in data:
        for category in scores.keys():
            if category in item:
                scores[category].append(item[category]["average_score"])

    mean_std = {category: {"mean": np.mean(scores[category]), "std": np.std(scores[category])} for category in scores}
    return scores, mean_std

filename1  = "evaluation_reproduce_all_25_3"
filename2 = "evaluation_reproduce_yes_extracted_25_3"
# File paths
#file_path_current = '/home/chenlawrance/repo/LLM-Creativity/eval_api/result/evaluation_Curr_classify_answers_50_3.json'
#file_path_previous = '/home/chenlawrance/repo/LLM-Creativity/eval_api/result/evaluation_Prev_classify_answers_50_3.json'

file_path_current = f'/home/chenlawrance/repo/LLM-Creativity/eval_api/result/{filename1}'
file_path_previous = f'/home/chenlawrance/repo/LLM-Creativity/eval_api/result/{filename2}'


# Calculate for current and previous files
scores_current, mean_std_current = calculate_mean_std(file_path_current)
scores_previous, mean_std_previous = calculate_mean_std(file_path_previous)

# Plotting box plots
categories = ["fluency", "flexibility", "originality", "elaboration"]
for category in categories:
    plt.figure()
    
    # Combine current and previous scores for box plotting
    data_to_plot = [scores_current[category], scores_previous[category]]

    # Create the box plot
    plt.boxplot(data_to_plot, patch_artist=True)

    # Customizing the box plot
    plt.xticks([1, 2], [filename1, filename2])
    plt.title(f"{category.capitalize()} Scores Box Plot")
    plt.ylabel('Score')

    # Save the plot as an image
    plt.savefig(f"/home/chenlawrance/repo/LLM-Creativity/eval_api/analysis_img/boxplot/{filename1}_{filename2}_{category}_boxplot.png")

# Print the mean and standard deviation
print(filename1)
for category in mean_std_current:
    print(f"{category} - Mean: {mean_std_current[category]['mean']}, Standard Deviation: {mean_std_current[category]['std']}")

print(filename2)
for category in mean_std_previous:
    print(f"{category} - Mean: {mean_std_previous[category]['mean']}, Standard Deviation: {mean_std_previous[category]['std']}")
