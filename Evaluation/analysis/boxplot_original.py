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
        print(item["average_originality"])
        print(item["average_elaboration"])
        originality_scores.append(item["average_originality"])
        elaboration_scores.append(item["average_elaboration"])

    averages = {
        "originality": {"mean": np.mean(originality_scores), "std": np.std(originality_scores)},
        "elaboration": {"mean": np.mean(elaboration_scores), "std": np.std(elaboration_scores)}
    }
    return originality_scores, elaboration_scores, averages

if __name__ == "__main__":
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Find mean and standard deviation of sample JSON files")
    parser.add_argument("-i", "--input_files", nargs=2, required=True, help="File paths of the two JSON files")
    parser.add_argument("-t", "--type", choices=['default', 'sampling'], default='default', help="Type of evaluation")
    args = parser.parse_args()

    # Extract the two input files
    input_file_1, input_file_2 = args.input_files

    # Example usage of the extracted files
    print("Input file 1:", input_file_1)
    print("Input file 2:", input_file_2)
    if args.type == "sampling":
        # File paths
        file_path_1 = os.path.join(Path(__file__).parent,'..', 'result_sample', f"{input_file_1}.json")
        file_path_2 = os.path.join(Path(__file__).parent, '..','result_sample', f"{input_file_2}.json")
        print("file path 1:", file_path_1)
        print("file path 2:", file_path_2)
        originality_1, elaboration_1, averages_1 = calculate_mean_std_sampling(file_path_1)
        originality_2, elaboration_2, averages_2 = calculate_mean_std_sampling(file_path_2)

        # Plotting box plots for originality and elaboration
        categories = ["originality", "elaboration"]
        for category in categories:
            plt.figure()
            
            # Data for plotting
            data_to_plot = [originality_1, originality_2] if category == "originality" else [elaboration_1, elaboration_2]
            
            # Create the box plot
            plt.boxplot(data_to_plot, patch_artist=True)
            
            # NAME BOXPLOT
            plt.xticks([1, 2], ["FILE 1", "FILE 2"])
            plt.title(f"{category.capitalize()} Scores Box Plot")
            plt.ylabel('Score')
            image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot', 
                f"{input_file_1}_{input_file_2}_{category}_boxplot.png"
            )
            # Save or show the plot
            plt.savefig(image_path)
            # plt.show() # Uncomment to display the plot instead of saving

        # Print the mean and standard deviation
        print("Current Evaluation:")
        for category, stats in averages_1.items():
            print(f"{category} - Mean: {stats['mean']}, Standard Deviation: {stats['std']}")

        print("\nPrevious Evaluation:")
        for category, stats in averages_2.items():
            print(f"{category} - Mean: {stats['mean']}, Standard Deviation: {stats['std']}")


    elif args.type == "default":
        # File paths
        file_path_current = os.path.join(Path(__file__).parent, 'result', f"{input_file_1}.json")
        file_path_previous = os.path.join(Path(__file__).parent, 'result', f"{input_file_2}.json")

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
            # NAME BOXPLOT
            plt.xticks([1, 2], ["FILE 1", "FILE 2"])
            plt.title(f"{category.capitalize()} Scores Box Plot")
            plt.ylabel('Score')

            image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot', 
                f"{input_file_1}_{input_file_2}_{category}_boxplot.png"
            )
            # Save the plot as an image
            plt.savefig(image_path)

        # Print the mean and standard deviation
        print(input_file_1)
        for category in mean_std_current:
            print(f"{category} - Mean: {mean_std_current[category]['mean']}, Standard Deviation: {mean_std_current[category]['std']}")

        print(input_file_2)
        for category in mean_std_previous:
            print(f"{category} - Mean: {mean_std_previous[category]['mean']}, Standard Deviation: {mean_std_previous[category]['std']}")
    

# python3 boxplot.py -i file1 file2 -t sampling
# file1 and file2 are the names of the JSON files to be compared
# file1 and file2 are saved in the result folder