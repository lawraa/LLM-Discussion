import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import argparse

def calculate_mean_std(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    fluency_scores = []
    flexibility_scores = []
    originality_scores = []
    elaboration_scores = []

    for item in data:
        if 'fluency' in item:
            for fluency in item['fluency']:
                if 'average_fluency' in fluency:
                    fluency_scores.append(fluency['average_fluency'])
        if 'flexibility' in item:
            for flexibility in item['flexibility']:
                if 'average_flexibility' in flexibility:
                    flexibility_scores.append(flexibility['average_flexibility'])
        if 'originality' in item:
            for originality in item['originality']:
                if 'average_originality' in originality:
                    originality_scores.append(originality['average_originality'])
        if 'elaboration' in item:
            for elaboration in item['elaboration']:
                if 'average_elaboration' in elaboration:
                    elaboration_scores.append(elaboration['average_elaboration'])

    averages = {
        "fluency": {"mean": np.mean(fluency_scores), "std": np.std(fluency_scores)},
        "flexibility": {"mean": np.mean(flexibility_scores), "std": np.std(flexibility_scores)},
        "originality": {"mean": np.mean(originality_scores), "std": np.std(originality_scores)},
        "elaboration": {"mean": np.mean(elaboration_scores), "std": np.std(elaboration_scores)}
    }
    return fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages

def plot_scores(scores, category):
    plt.figure(figsize=(10, 6))
    plt.boxplot(scores, vert=False, patch_artist=True)
    plt.title(f'Boxplot of {category}')
    image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot', 
                f"{category}_boxplot_feb_21.png"
            )
    plt.savefig(image_path)

def plot_scores_side_by_side(scores_dict, category):
    fig, ax = plt.subplots(figsize=(10, 6))
    data_to_plot = [scores for scores in scores_dict.values()]
    ax.boxplot(data_to_plot, patch_artist=True)
    ax.set_xticklabels(scores_dict.keys())
    plt.title(f'Boxplot of {category} Across Multiple Files')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to not cut off labels
    image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot', 
                f"{category}_boxplot_feb_21.png"
            )
    plt.savefig(image_path)
    plt.show()

# help me write the code the reads a json file and returns the scores and the mean and std of the scores of "average_fluency","average_flexibility","average_originality", "average_elaboration" , then a code for plotting the boxplot for each of them 
def main(input_files):
    all_scores = []
    all_fluency_scores = {}
    all_flexibility_scores = {}
    all_originality_scores = {}
    all_elaboration_scores = {}

    for file_name in input_files:
        file_path = os.path.join(Path(__file__).parent, '..', 'result', f"{file_name}.json")
        fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages = calculate_mean_std(file_path)

        # Store scores from each file
        all_fluency_scores[file_name] = fluency_scores
        all_flexibility_scores[file_name] = flexibility_scores
        all_originality_scores[file_name] = originality_scores
        all_elaboration_scores[file_name] = elaboration_scores

    plot_scores_side_by_side(all_fluency_scores, "Fluency")
    plot_scores_side_by_side(all_flexibility_scores, "Flexibility")
    plot_scores_side_by_side(all_originality_scores, "Originality")
    plot_scores_side_by_side(all_elaboration_scores, "Elaboration")

    for file_name in input_files:
        file_path = os.path.join(Path(__file__).parent, '..', 'result', f"{file_name}.json")
        fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages = calculate_mean_std(file_path)

    plot_scores(fluency_scores, "Fluency")
    plot_scores(flexibility_scores, "Flexibility")
    plot_scores(originality_scores, "Originality")
    plot_scores(elaboration_scores, "Elaboration")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple JSON files for scoring analysis.")
    parser.add_argument("-i", "--input_files", nargs='+', required=True, help="File paths of the JSON files")
    args = parser.parse_args()

    main(args.input_files)
