import csv
import glob
import json
import numpy as np

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
        "fluency": {"mean": round(np.mean(fluency_scores), 2), "std": round(np.std(fluency_scores), 2)},
        "flexibility": {"mean": round(np.mean(flexibility_scores), 2), "std": round(np.std(flexibility_scores), 2)},
        "originality": {"mean": round(np.mean(originality_scores), 2), "std": round(np.std(originality_scores), 2)},
        "elaboration": {"mean": round(np.mean(elaboration_scores), 2), "std": round(np.std(elaboration_scores), 2)}
    }   

    return fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages


input_paths = glob.glob("./tmp/*")

for input_file_name in input_paths:
    data = []
    fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages = calculate_mean_std(input_file_name)

    input_file_name = input_file_name.split('_')[1:]
    # print(input_file_name)

    Task_Type = input_file_name[0]
    Subtask_Type = input_file_name[2]

    Agent = input_file_name[1]
    
    version = 3.5
    if Agent == "single":
        Agent = 1
        rounds = 1
        Agent_Description = f"gpt-{version}-turbo"
    # elif Agent == 'multi':
    #     Agent = input_file_name[3]
    #     rounds = input_file_name[4]
    #     Agent_Description = f"gpt-{version}, gpt-{version}"
    # else:
    #     print('ERROR AGENT!!')

    # data_num = input_file_name[3].split('-')[0]

    # prompt = input_file_name.split('_')[-6]
    # print(prompt)
    # Task_Type = 'AUT'
    # Subtask_Type = 'round-test'
    # Agent = 2
    # Agent_Description = 'gpt-3.5, gpt-3.5'
    data_num = 100
    # rounds = 6
    # rounds = input_file_name.split('_')[-4]
    # print(rounds)

    # row = [Task_Type, f"{Subtask_Type}-{prompt}", Agent, Agent_Description, data_num, rounds, 
    row = [Task_Type, f"{Subtask_Type}", Agent, Agent_Description, data_num, rounds, 
            averages['fluency']['mean'], averages['flexibility']['mean'], averages['originality']['mean'], averages['elaboration']['mean'], averages['fluency']['std'], averages['flexibility']['std'], averages['originality']['std'], averages['elaboration']['std']]

    print(row)

    with open(f"./LeaderBoard-{Task_Type}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)


csv_file_path = './LeaderBoard-AUT.csv'
sorted_csv_file_path = csv_file_path

data = []
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)  
    for row in reader:
        data.append(row)

sorted_data = sorted(data, key=lambda x: (int(x[2]), int(x[4]), x[1], int(x[4]), x[5]))

with open(sorted_csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(sorted_data)

print(f'Data sorted by Task_Type and Data and saved to {sorted_csv_file_path}')
