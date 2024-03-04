import csv
import glob
import json
import numpy as np

input_paths = glob.glob("./tmp/*")

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

    # averages = {
    #     "fluency": {"mean": np.mean(fluency_scores), "std": np.std(fluency_scores)},
    #     "flexibility": {"mean": np.mean(flexibility_scores), "std": np.std(flexibility_scores)},
    #     "originality": {"mean": np.mean(originality_scores), "std": np.std(originality_scores)},
    #     "elaboration": {"mean": np.mean(elaboration_scores), "std": np.std(elaboration_scores)}
    # }
    averages = {
        "fluency": {"mean": round(np.mean(fluency_scores), 2), "std": round(np.std(fluency_scores), 2)},
        "flexibility": {"mean": round(np.mean(flexibility_scores), 2), "std": round(np.std(flexibility_scores), 2)},
        "originality": {"mean": round(np.mean(originality_scores), 2), "std": round(np.std(originality_scores), 2)},
        "elaboration": {"mean": round(np.mean(elaboration_scores), 2), "std": round(np.std(elaboration_scores), 2)}
    }   

    return fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages

for input_file_name in input_paths:
    data = []
    fluency_scores, flexibility_scores, originality_scores, elaboration_scores, averages = calculate_mean_std(input_file_name)

    # input_file_name = input_file_name.split('_')[2:]

    # Task_Type = input_file_name[0]
    # Subtask_Type = input_file_name[2]

    # Agent = input_file_name[1]
    
    # version = 3.5
    # if Agent == "single":
    #     Agent = 1
    #     rounds = 1
    #     Agent_Description = f"gpt-{version}"
    # elif Agent == 'multi':
    #     Agent = input_file_name[3]
    #     rounds = input_file_name[4]
    #     Agent_Description = f"gpt-{version}, gpt-{version}"
    # else:
    #     print('ERROR AGENT!!')

    # data_num = input_file_name[3].split('-')[0]

    # prompt = input_file_name.split('_')[-6]
    # print(prompt)
    Task_Type = 'AUT'
    Subtask_Type = 'round-test'
    Agent = 2
    Agent_Description = 'gpt-3.5, gpt-3.5'
    data_num = 10
    # rounds = 6
    rounds = input_file_name.split('_')[-4]
    # print(rounds)

    # row = [Task_Type, f"{Subtask_Type}-{prompt}", Agent, Agent_Description, data_num, rounds, 
    row = [Task_Type, f"{Subtask_Type}", Agent, Agent_Description, data_num, rounds, 
            averages['fluency']['mean'], averages['flexibility']['mean'], averages['originality']['mean'], averages['elaboration']['mean'], averages['fluency']['std'], averages['flexibility']['std'], averages['originality']['std'], averages['elaboration']['std']]

    print(row)

    with open("./unsorted-LeaderBoard.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)