import pickle
import json

# Load data from the pickle file
with open('cache_3.pickle', 'rb') as file1:
    data1 = pickle.load(file1)

# Save the data as a JSON file
with open('cache_json.json', 'w') as json_file:
    json.dump(data1, json_file)
