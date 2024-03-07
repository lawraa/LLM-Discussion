import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

def plot_mean_std_for_each_category(df, score_category, output_folder, dataset):
    # Create a figure and an axis object
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract the subtask types and data
    subtask_data_pairs = df[['Subtask_type', 'Data']].drop_duplicates()
    
    # Plot each mean with std deviation as error bar
    for index, (subtask, data) in enumerate(subtask_data_pairs.values):
        # Filter rows for the current subtask and data
        subtask_rows = df[(df['Subtask_type'] == subtask) & (df['Data'] == data)]
        
        # Calculate the mean and std deviation for the score category
        mean = subtask_rows[f'mean_{score_category}'].mean()
        std = subtask_rows[f'std_{score_category}'].mean()

        # Plot the error bar for the current subtask and data
        ax.errorbar(index, mean, yerr=std, fmt='o', color='blue', ecolor='lightgray', elinewidth=3, capsize=5)
        
        # Annotate the mean and std deviation on the plot
        ax.annotate(f'Mean: {mean:.2f}\nStd: {std:.2f}', 
                    (index, mean), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center')

    # Set the x-tick labels
    ax.set_xticks(range(len(subtask_data_pairs)))
    ax.set_xticklabels([f"{st}-{d}" for st, d in subtask_data_pairs.values], rotation=45, ha='right')
    
    # Set title and y-label
    ax.set_title(f"{score_category.capitalize()} Scores of {dataset}")
    ax.set_ylabel(score_category.capitalize() + " Score")
    
    # Save the figure
    plt.tight_layout()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, f"{dataset}_{score_category}_Mean_Std_Distribution-2.png")
    plt.savefig(output_path)
    plt.close(fig)  # Close the figure to free memory

    print(f"Mean and Std Dev plot saved at {output_path}")
    

def plot_combined_mean_std(df, categories, output_folder, dataset):
    # Define the size of the entire figure grid
    fig, axs = plt.subplots(2, 2, figsize=(30, 20))  # For instance, a 15x10 figure with 4 subplots
    axs = axs.flatten()  # Flatten the array for easy iteration
    
    for index, score_category in enumerate(categories):
        ax = axs[index]  # Select the appropriate subplot
        subtask_data_pairs = df[['Subtask_type', 'Data']].drop_duplicates()
        
        for i, (subtask, data) in enumerate(subtask_data_pairs.values):
            subtask_rows = df[(df['Subtask_type'] == subtask) & (df['Data'] == data)]
            mean = subtask_rows[f'mean_{score_category}'].mean()
            std = subtask_rows[f'std_{score_category}'].mean()
            ax.errorbar(i, mean, yerr=std, fmt='o', color='blue', ecolor='lightgray', elinewidth=3, capsize=5)
            ax.annotate(f'Mean: {mean:.2f}\nStd: {std:.2f}', (i, mean), textcoords="offset points", xytext=(0,10), ha='center', fontsize=12)
        
        ax.set_xticks(range(len(subtask_data_pairs)))
        ax.set_xticklabels([f"{st}-{d}" for st, d in subtask_data_pairs.values], rotation=45, ha='right')
        ax.set_title(f"{score_category.capitalize()} Scores of {dataset}")
        ax.set_ylabel(score_category.capitalize() + " Score")
    
    plt.tight_layout()
    combined_output_path = os.path.join(output_folder, f"{dataset}_Combined_Mean_Std_Distribution.png")
    plt.savefig(combined_output_path)
    plt.close(fig)  # Close the figure to free memory
    print(f"Combined Mean and Std Dev plot saved at {combined_output_path}")

def main(csv_file_path, output_folder, dataset):
    df = pd.read_csv(csv_file_path)
    categories = ['fluency', 'flexibility', 'originality', 'elaboration']
    
    # Create individual plots for each category
    for category in categories:
        plot_mean_std_for_each_category(df, category, output_folder, dataset)
    
    # Create a combined plot for all categories
    plot_combined_mean_std(df, categories, output_folder, dataset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", default="AUT", choices=["AUT", "Instances", "Similarities", "scientific"], help="Input the dataset you want to plot")
    args = parser.parse_args()

    csv_file_path = f'../LeaderBoard-{args.dataset}.csv'
    output_folder = f'./{args.dataset}/'
    main(csv_file_path, output_folder, args.dataset)