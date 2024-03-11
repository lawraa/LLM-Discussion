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

def plot_score(scores_dict, category, custom_xtick_labels=None, output_name=None, title=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    data_to_plot = [scores for scores in scores_dict.values()]
    ax.boxplot(data_to_plot, patch_artist=True)

    new_xtick_labels = []
    for scores in data_to_plot:
        mean = np.mean(scores)
        std = np.std(scores)
        label = f'Mean: {mean:.2f}\nStd: {std:.2f}'
        new_xtick_labels.append(label)

    if custom_xtick_labels and len(custom_xtick_labels) == len(scores_dict):
        combined_labels = [f'{custom}\n\n{new}' for custom, new in zip(custom_xtick_labels, new_xtick_labels)]
        ax.set_xticklabels(combined_labels, ha='center',fontsize=12)
    else:
        original_labels = list(scores_dict.keys())
        combined_labels = [f'{orig}\n\n{new}' for orig, new in zip(original_labels, new_xtick_labels)]
        ax.set_xticklabels(combined_labels, rotation=45, ha='right',fontsize=12)

    plt.title(f'{category}: {title}', fontsize = 20)
    plt.ylabel('Score')
    plt.xticks()
    plt.tight_layout()  # Adjust layout to not cut off labels
    

    image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot', 
                f"{category}_{output_name}.png"
            )
    plt.savefig(image_path)
    print(f"Boxplot for {category} saved at {image_path}") 
    #plt.show()

def plot_combined_subplots(scores_dicts, custom_xtick_labels, output_name, title):
    fig, axs = plt.subplots(2, 2, figsize=(20, 12))
    categories = ["Fluency", "Flexibility", "Originality", "Elaboration"]

    for i, (ax, category) in enumerate(zip(axs.flatten(), categories)):
        scores = scores_dicts[category]
        data_to_plot = [score for score in scores.values()]
        ax.boxplot(data_to_plot, patch_artist=True)
        
        new_xtick_labels = []
        for score in data_to_plot:
            mean = np.mean(score)
            std = np.std(score)
            label = f'Mean: {mean:.2f}\nStd: {std:.2f}'
            new_xtick_labels.append(label)

        if custom_xtick_labels and len(custom_xtick_labels) == len(scores):
            combined_labels = [f'{custom}\n\n{new}' for custom, new in zip(custom_xtick_labels, new_xtick_labels)]
            ax.set_xticklabels(combined_labels, ha='center', fontsize=12)
        else:
            original_labels = list(scores.keys())
            combined_labels = [f'{orig}\n\n{new}' for orig, new in zip(original_labels, new_xtick_labels)]
            ax.set_xticklabels(combined_labels, rotation=45, ha='right', fontsize=12)

        ax.set_title(f'{category}: {title}', fontsize=20)
        ax.set_ylabel('Score')

    plt.tight_layout()  # Adjust layout to not cut off labels
    combined_image_path = os.path.join(
                Path(__file__).parent, 'img', 'boxplot',
                f"Combined_{output_name}.png"
            )
    plt.savefig(combined_image_path)
    print(f"Combined plot saved at {combined_image_path}")
    plt.close(fig)



def main(input_files, output_name, custom_labels, title):
    all_fluency_scores = {}
    all_flexibility_scores = {}
    all_originality_scores = {}
    all_elaboration_scores = {}

    print("CUSTOM LABEL:", custom_labels, "\n", "OUTPUT_NAME:", output_name, "\n", "TITLE:", title, "\n", "INPUT_FILES:", input_files, "\n")

    for file_name in input_files:
        file_path = file_name
        fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages = calculate_mean_std(file_path)

        # Store scores from each file
        all_fluency_scores[file_name] = fluency_scores
        all_flexibility_scores[file_name] = flexibility_scores
        all_originality_scores[file_name] = originality_scores
        all_elaboration_scores[file_name] = elaboration_scores

        print("File: ", file_name)
        print("Average: ", averages, "\n")

    scores_dicts = {
        "Fluency": all_fluency_scores,
        "Flexibility": all_flexibility_scores,
        "Originality": all_originality_scores,
        "Elaboration": all_elaboration_scores
    }

    plot_score(all_fluency_scores, "Fluency",custom_labels, output_name, title)
    plot_score(all_flexibility_scores, "Flexibility",custom_labels, output_name, title)
    plot_score(all_originality_scores, "Originality",custom_labels, output_name, title)
    plot_score(all_elaboration_scores, "Elaboration",custom_labels, output_name, title)
    plot_combined_subplots(scores_dicts, custom_labels, output_name, title)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Process multiple JSON files for scoring analysis.")
    # parser.add_argument("-i", "--input_files", nargs='+', required=True, help="File paths of the JSON files")
    # parser.add_argument("-o", "--output_name", required=True, help="Give me the name of the output file without using json")
    # parser.add_argument("-l", "--custom_labels", nargs='+', required=False, help="Give me the custom labels for the boxplot")
    # parser.add_argument("-t", "--title", required=False, help="Give me the title of the plot")
    # args = parser.parse_args()
    # main(args.input_files, args.output_name, args.custom_labels, args.title)
    
    # Lazy to write all the arguments, so I just hardcode them
    input_files = ['/Users/lawrancechen/Desktop/CreativeLM/NewRepo/LLM-Creativity/Results/AUT/Eval_Result/multi_agent/evaluation_AUT_multi_debate_default_2_3_gpt-3-5-turbo_None-None_final_2024-03-11-09-17-40_1_sampling_3.json', 
                   '/Users/lawrancechen/Desktop/CreativeLM/NewRepo/LLM-Creativity/Results/AUT/Eval_Result/multi_agent/evaluation_AUT_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gemini-pro_discussion_final_without_special_prompts_10_sampling_3.json']  # Example file paths
    custom_labels = ['Label 1', 'Label 2']  # These must match the number of input files if they are used
    output_name = 'analysis_result'
    title = 'My Analysis'

    main(input_files, output_name, custom_labels, title)

    
