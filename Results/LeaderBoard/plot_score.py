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

    csv_file_path = f'./LeaderBoard-{args.dataset}.csv'
    output_folder = f'./plots/{args.dataset}/'
    main(csv_file_path, output_folder, args.dataset)



# version 1st ==========================================================
# def plot_boxplot_for_each_category(df, score_category, output_folder):
#     # Create a figure and an axis object
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # Store the data to plot
#     data_to_plot = []
#     # New approach: Integrate mean and std into xticklabels directly
#     combined_xticklabels = []
    
#     # Extract the subtask types and data to construct the x-tick labels
#     subtask_data_pairs = df[['Subtask_type', 'Data']].drop_duplicates()
    
#     for _, row in subtask_data_pairs.iterrows():
#         subtask_label = f"{row['Subtask_type']}-{row['Data']}"
#         # Get the rows corresponding to this subtask type and data
#         subtask_rows = df[(df['Subtask_type'] == row['Subtask_type']) & (df['Data'] == row['Data'])]
#         # Append the scores for this subtask type and data
#         data_to_plot.append(subtask_rows[f'mean_{score_category}'].values)
#         mean = subtask_rows[f'mean_{score_category}'].mean()
#         std = subtask_rows[f'std_{score_category}'].mean()
#         # New: combine subtask label with mean and std
#         combined_label = f"{subtask_label}\nMean: {mean:.2f}\nStd: {std:.2f}"
#         combined_xticklabels.append(combined_label)
    
#     # Plot the boxplots
#     ax.boxplot(data_to_plot, patch_artist=True)
#     # Use the combined labels as xticklabels
#     ax.set_xticklabels(combined_xticklabels, rotation=45, ha='right')
    
#     # Set title and axis labels
#     ax.set_title(f"{score_category.capitalize()}: Score Distribution by Subtask Type")
#     ax.set_ylabel("Score")
    
#     # Save the figure
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_folder, f"{score_category}_Score_Distribution_Modified.png"))
#     plt.close()  # Close the figure to free memory

# version 2nd ==========================================================
# def plot_mean_std_for_each_category(df, score_category, output_folder):
#     # Create a figure and an axis object
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # Store the data to plot: mean values and std deviation
#     means = []
#     stds = []
#     x_labels = []
    
#     # Extract the subtask types and data to construct the x-tick labels
#     subtask_data_pairs = df[['Subtask_type', 'Data']].drop_duplicates()
    
#     for index, (subtask, data) in enumerate(subtask_data_pairs.values):
#         # Get the rows corresponding to this subtask type and data
#         subtask_rows = df[(df['Subtask_type'] == subtask) & (df['Data'] == data)]
        
#         # Calculate the mean and std deviation for the score category
#         mean = subtask_rows[f'mean_{score_category}'].mean()
#         std = subtask_rows[f'std_{score_category}'].mean()
#         means.append(mean)
#         stds.append(std)
        
#         # Construct the x-tick label for this subtask and data combination
#         x_labels.append(f"{subtask}-{data}\nMean: {mean:.2f}\nStd: {std:.2f}")

#     # Plot the mean and std deviation as error bars
#     # 'capsize' specifies the width of the caps on the error bars
#     ax.errorbar(range(len(means)), means, yerr=stds, fmt='o', color='blue', ecolor='lightgray', elinewidth=3, capsize=5)

#     # Set the x-tick labels to the previously constructed labels
#     ax.set_xticks(range(len(x_labels)))
#     # ax.set_xticklabels(x_labels, rotation=45, ha='right')
#     ax.set_xticklabels(x_labels)
    
#     # Set the title and the y-label
#     ax.set_title(f"{score_category.capitalize()} Scores with Mean and Std Dev")
#     ax.set_ylabel(score_category.capitalize() + " Score")

#     # Save the figure
#     plt.tight_layout()
#     output_path = os.path.join(output_folder, f"{score_category}_Mean_Std_Distribution.png")
#     plt.savefig(output_path)
#     plt.close()  # Close the figure to free memory

#     print(f"Mean and Std Dev plot saved at {output_path}")