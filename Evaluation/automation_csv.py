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
        "mean_fluency": round(np.mean(fluency_scores), 2),
        "std_fluency": round(np.std(fluency_scores), 2),
        "mean_flexibility": round(np.mean(flexibility_scores), 2),
        "std_flexibility": round(np.std(flexibility_scores), 2),
        "mean_originality": round(np.mean(originality_scores), 2),
        "std_originality": round(np.std(originality_scores), 2),
        "mean_elaboration": round(np.mean(elaboration_scores), 2),
        "std_elaboration": round(np.std(elaboration_scores), 2),
    }
    return results
# round(np.mean(fluency_scores), 2)

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
        Agent_Description = "gpt-3.5" if version == 3 else "gpt-4"
        # Agent_Description = f"gpt-{version}"
    elif Agent == 'multi':
        Agent = input_file_name.split('_')[3]
        rounds = input_file_name.split('_')[4]
        Agent_Description = input_file_name.split('_')[5]
        # Agent_Description = f"gpt-{version}, gpt-{version}"
    else:
        print('ERROR AGENT!!')

    
    # Agent_Description = "gpt-3.5"
    data_num = input_file_name.split('_')[-1].split('-')[0]
    

    row = [Task_Type, Subtask_Type, Agent, Agent_Description, data_num, rounds]
    row.extend([results[key] for key in sorted(results.keys())])  # Ensure the order is correct
    row.extend([])
    csv_data.append(row)

    print(csv_file_path)

    # Writing to CSV file
    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    
    # sort the leader board
    data = []
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  
        for row in reader:
            data.append(row)

    sorted_data = sorted(data, key=lambda x: (int(x[2]), int(x[4]), x[1],  x[5]))

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)

    print(f'Data sorted by Task_Type and Data and saved to {csv_file_path}')

        # python3 auto_grade_bai.py -v 3 -i Instances_single_few-shot_2-0 -t sampling -s 3 -d Instances
        # python3 auto_grade_bai.py -v 3 -i Instances_multi_debate_2_3_discussion_final_3-0 -t sampling -s 3 -d Instances
