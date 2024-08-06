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
        "mean_fluency": round(np.mean(fluency_scores), 3),
        "std_fluency": round(np.std(fluency_scores), 3),
        "mean_flexibility": round(np.mean(flexibility_scores), 3),
        "std_flexibility": round(np.std(flexibility_scores), 3),
        "mean_originality": round(np.mean(originality_scores), 3),
        "std_originality": round(np.std(originality_scores), 3),
        "mean_elaboration": round(np.mean(elaboration_scores), 3),
        "std_elaboration": round(np.std(elaboration_scores), 3),
    }
    return results

def write_results_to_csv(input_file_name, mean_std_results, csv_file_path, version):
    
    headers = ['Timestamp', 'Task', 'Type', 'Mode', 'Agent', 'Round','Model Name', 'Role Name', 'Data Num', 'Mean Fluency', 'STD Fluency', 'Mean Flexibility', 'STD Flexibility', 'Mean Originality', 'STD Originality', 'Mean Elaboration', 'STD Elaboration', 'File Name']
    csv_data = []
    parts = input_file_name.split('_')


    Task = parts[0] # AUT, Scientific, Similarities, Instances
    Type = parts[2] # debate, conversational
    Data_Num = parts[-1].split('-')[0]
    Raw_Timestamp = parts[-2].split('-')
    print("Raw_Timestamp: ", Raw_Timestamp)
    date = '-'.join(Raw_Timestamp[:3])
    print("date: ", date)
    time = ':'.join(Raw_Timestamp[3:6])
    print("time: ", time)
    Timestamp = f'{date} {time}'

    Mode, Agent, Rounds, Model_Name, Role_Name = None, None, None, None, None  # Initialize to None

    if parts[1] == "single":
        Agent = parts[4]
        Rounds = parts[5]
        Model_Name = parts[6]
        Mode = parts[3]
        Role_Name = parts[7]
    if parts[1] == 'multi':
        Mode = parts[3]
        Agent = parts[4]
        Rounds = parts[5]
        Model_Name = parts[6]
        Role_Name = parts[7]
    else:
        print('ERROR AGENT!!')
    

    row = [Timestamp, Task, Type, Mode, Agent, Rounds, Model_Name, Role_Name, Data_Num]
    row.extend([
        mean_std_results['mean_fluency'], mean_std_results['std_fluency'],
        mean_std_results['mean_flexibility'], mean_std_results['std_flexibility'],
        mean_std_results['mean_originality'], mean_std_results['std_originality'],
        mean_std_results['mean_elaboration'], mean_std_results['std_elaboration'],
        input_file_name 
    ])
    csv_data.append(row)
    file_path = Path(csv_file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with file_path.open(mode='a+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If file is empty, write headers
                writer.writerow(headers)
            writer.writerows(csv_data)
        
        # Now sort the data if needed, by reading, sorting, and rewriting the CSV file
        with file_path.open(mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            sorted_data = sorted(reader, key=lambda x: (x[0], x[8]))  # Sort by Timestamp and Data Num

        with file_path.open(mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write headers
            writer.writerows(sorted_data)

        print(f'Data sorted by Timestamp and Data and saved to {csv_file_path}')
    except Exception as e:
        print(f'ERROR: Failed to write data to CSV due to {e}')

    print(f'Data sorted by Timestamp and Data and saved to {csv_file_path}')
