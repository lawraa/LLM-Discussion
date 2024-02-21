import json

file_path = '../../../eval_api/result/evaluation_discussion_final_results_02-21_2_2_sampling_3_sample.json'

with open(file_path, 'r') as f:
    data = json.load(f)

print(f"There're {len(data)} answers")
print(data[0].keys())

originality = 0
elaboration = 0
flexibility = 0
fluency = 0

for item in data:
    # print(item['item'])
    print('average_originality:', item['originality'][-1]['average_originality'])
    print('average_elaboration:', item['elaboration'][-1]['average_elaboration'])
    print('average_flexibility:', item['flexibility'][-1]['average_flexibility'])
    print('average_fluency:', item['fluency'][-1]['average_fluency'])
    print()
    # print(item.keys())

    originality += item['originality'][-1]['average_originality']
    elaboration += item['elaboration'][-1]['average_elaboration']
    flexibility += item['flexibility'][-1]['average_flexibility']
    fluency += item['fluency'][-1]['average_fluency']

avg_originality = originality/len(data)
avg_elaboration = elaboration/len(data)
avg_flexibility = flexibility/len(data)
avg_fluency = fluency/len(data)

print(f"avg_originality: {avg_originality}")
print(f"avg_elaboration: {avg_elaboration}")
print(f"avg_flexibility: {avg_flexibility}")
print(f"avg_fluency: {avg_fluency}")
