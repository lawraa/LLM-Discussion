import csv

# 路徑可能需要根據您的文件系統進行調整
csv_file_path = './LeaderBoard.csv'
sorted_csv_file_path = './SortedLeaderBoard.csv'

data = []
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)  
    for row in reader:
        data.append(row)

sorted_data = sorted(data, key=lambda x: (x[0], int(x[4])))

with open(sorted_csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(sorted_data)

print(f'Data sorted by Task_Type and Data and saved to {sorted_csv_file_path}')
