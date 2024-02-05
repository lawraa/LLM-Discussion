import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import argparse

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

def calculate_mean_std_sampling(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    originality_scores = []
    elaboration_scores = []

    for item in data:
        originality_scores.append(item.get("average_originality", 0))
        elaboration_scores.append(item.get("average_elaboration", 0))

    averages = {
        "originality": {"mean": np.mean(originality_scores), "std": np.std(originality_scores)},
        "elaboration": {"mean": np.mean(elaboration_scores), "std": np.std(elaboration_scores)}
    }
    return originality_scores, elaboration_scores, averages

def main(input_files, evaluation_type):
    all_scores = []
    all_averages = []

    for file_name in input_files:
        file_path = os.path.join(Path(__file__).parent, '..', 'result', f"{file_name}.json")
        if evaluation_type == "sampling":
            originality_scores, elaboration_scores, averages = calculate_mean_std_sampling(file_path)
            all_scores.append((originality_scores, elaboration_scores))
            all_averages.append(averages)
        else:
            scores, mean_std = calculate_mean_std(file_path)
            all_scores.append(scores)
            all_averages.append(mean_std)

    # Plotting logic here, adjusted to handle multiple files
    if evaluation_type == "sampling":
        categories = ["originality", "elaboration"]
    else:
        categories = ["fluency", "flexibility", "originality", "elaboration"]

    for category in categories:
        plt.figure()
        if category in ["originality", "elaboration"]:  # For sampling evaluation
            data_to_plot = [scores[0] for scores in all_scores] if category == "originality" else [scores[1] for scores in all_scores]
        else:
            data_to_plot = [scores[0] for scores in all_scores] if category == "fluency" else [scores[1] for scores in all_scores]
        plt.boxplot(data_to_plot, patch_artist=True)
        plt.xticks(range(1, len(input_files) + 1), [f"FILE {i+1}" for i in range(len(input_files))])
        plt.title(f"{category.capitalize()} Scores Box Plot")
        plt.ylabel('Score')
        image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot', 
                f"{category}_boxplot.png"
            )
            # Save the plot as an image
        plt.savefig(image_path)
        #plt.show()

    # Example output of means and stds
    for idx, averages in enumerate(all_averages):
        print(f"File {idx + 1}:")
        for category, stats in averages.items():
            print(f"{category} - Mean: {stats['mean']}, Standard Deviation: {stats['std']}")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple JSON files for scoring analysis.")
    parser.add_argument("-i", "--input_files", nargs='+', required=True, help="File paths of the JSON files")
    parser.add_argument("-t", "--type", choices=['default', 'sampling'], default='default', help="Type of evaluation")
    args = parser.parse_args()

    main(args.input_files, args.type)
