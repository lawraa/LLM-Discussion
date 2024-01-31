import pickle
with open('cache_3.pickle', 'rb') as file1:
    data1 = pickle.load(file1)

with open('cache_35.pickle', 'rb') as file2:
    data2 = pickle.load(file2)

# Merge the dictionaries while updating values for matching keys
for key, value in data2.items():
    if key in data1:
        # Append the values if both keys match
        data1[key].extend(value)
    else:
        # Add the new key-value pair if it doesn't exist in data1
        data1[key] = value

# Save the combined dictionary to a new pickle file
with open('cache_3_2.pickle', 'wb') as combined_file:
    pickle.dump(data1, combined_file)

