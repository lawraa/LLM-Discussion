from pathlib import Path
import numpy as np
import csv


def calculate_mean_std(total_results):
    # Extracting scores for each criterion from the total results
    fluency_scores = [item["fluency"][-1]["average_fluency"] for item in total_results]
    print(fluency_scores)
    flexibility_scores = [item["flexibility"][-1]["average_flexibility"] for item in total_results]
    print(flexibility_scores)
    originality_scores = [item["originality"][-1]["average_originality"] for item in total_results]
    elaboration_scores = [item["elaboration"][-1]["average_elaboration"] for item in total_results]

    # Calculating mean and standard deviation for each criterion
    results = {
        "mean_fluency": np.mean(fluency_scores),
        "std_fluency": np.std(fluency_scores),
        "mean_flexibility": np.mean(flexibility_scores),
        "std_flexibility": np.std(flexibility_scores),
        "mean_originality": np.mean(originality_scores),
        "std_originality": np.std(originality_scores),
        "mean_elaboration": np.mean(elaboration_scores),
        "std_elaboration": np.std(elaboration_scores),
    }
    return results

def write_results_to_csv(input_file_name, results, csv_file_path, version):
    # Preparing data for CSV
    csv_data = []
    # csv_data = [
    #     ["Task_Type", "Subtask_type", "Agent", "Agent Description", "Data", "Rounds", "mean_fluency", "mean_flexibility", "mean_originality", "mean_elaboration", "std_fluency", "std_flexibility", "std_originality", "std_elaboration"]
    # ]

    
    print(input_file_name.split('_'))
    Task_Type = input_file_name.split('_')[0]
    Subtask_Type = input_file_name.split('_')[2]

    Agent = input_file_name.split('_')[1]
    if Agent == "single":
        Agent = 1
        rounds = 1
    elif Agent == 'multi':
        Agent = input_file_name.split('_')[3]
        rounds = input_file_name.split('_')[4]
    else:
        print('ERROR AGENT!!')

    Agent_Description = f"gpt-{version}"
    # Agent_Description = "gpt-3.5"
    data_num = input_file_name.split('_')[-1].split('-')[0]
    

    row = [Task_Type, Subtask_Type, Agent, Agent_Description, data_num, rounds]
    row.extend([results[key] for key in sorted(results.keys())])  # Ensure the order is correct
    row.extend([])
    csv_data.append(row)

    # Writing to CSV file
    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

        # python3 auto_grade_bai.py -v 3 -i Instances_single_few-shot_2-0 -t sampling -s 3 -d Instances
        # python3 auto_grade_bai.py -v 3 -i Instances_multi_debate_2_3_discussion_final_3-0 -t sampling -s 3 -d Instances
