import os
import re
import json
import glob
import datetime
import argparse
from tqdm import tqdm
from openai import OpenAI

client = OpenAI()

agent = 1

def write_output_file(results, purpose):
    folder_path = f"../../results/single_agent/{dataset}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if purpose == 'answer':
        base_file_name = f'{dataset}_single_result-{num}'
    elif purpose == 'history':
        base_file_name = f'{dataset}_single_history-{num}'

    file_extension = '.json'

    # ================== Handling repeated files ==================
    counter = 0
    file_name = f"{base_file_name}-{counter}{file_extension}"
    full_file_path = os.path.join(folder_path, file_name)

    while os.path.exists(full_file_path):
        counter += 1
        file_name = f"{base_file_name}-{counter}{file_extension}"
        full_file_path = os.path.join(folder_path, file_name)
    
    with open(full_file_path, "w") as outfile:
        json.dump(results, outfile, indent=4)
        print(f"output file save at: {full_file_path}")


def parsing_arg():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--dataset', type=str, default='AUT', help='Which dataset')
    parser.add_argument('-n', '--num', type=int, default=10, help='Number of questions')
    args = parser.parse_args()
    return args


def call_openai_api(prompt):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in API call: {e}")
        return None


def construct_assistant_message(completion):
    content = completion.choices[0].message.content
    return {"role": "assistant", "content": content}


def generate_answer(answer_context):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=answer_context,
            n=1)
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        return generate_answer(answer_context)
    return completion


def extract_uses(content):
    # Split the content into lines and remove the introductory sentence
    lines = content.split('\n')
    uses = [line.strip() for line in lines if line.strip() and re.match(r"^\d+\.", line)]

    # Remove the numbering from each use
    uses = [use[use.find('.') + 2:] for use in uses]
    return uses

    
def getting_answer(question, history, results, dataset, object_item):
    system_prompt = {"role": "system", "content": question}
    question += initial_prompt
    user_prompt = {"role": "user", "content": question}
    answer_context = [system_prompt, user_prompt]

    completion = generate_answer(answer_context)
    assistant_message = construct_assistant_message(completion)
    answers = extract_uses(assistant_message["content"])

    if dataset == 'AUT':
        history.append({
            f"item": object_item,
            "response": [line for line in assistant_message["content"].split('\n') if line.strip()],
        })
        
        results.append({
            f"item": object_item,
            "uses": answers,
        })

    else:
        history.append({
            f"question": question,
            "response": [line for line in assistant_message["content"].split('\n') if line.strip()],
        })

        results.append({
            f"question": question,
            "answer": answers,
        })


# ================================================== main function ==================================================
if __name__ == "__main__":
    args = parsing_arg()
    dataset = args.dataset
    num = args.num

    global results
    global history

    results = []
    history = []

    idx = 0
    initial_prompt = ' Please list the answer in 1. ... 2. ... 3. ... and so on.'

    input_file_name = f"../../datasets/{dataset}/{dataset.lower()}_{num}.json"
    with open(input_file_name, "r") as file:
        print(input_file_name)
        data = json.load(file)
    
    if dataset == 'AUT':
        for example in tqdm(data["Examples"], desc="Processing Examples"):
            idx += 1
            object_item = example["object"]
            problem_template = " ".join(data["Task"][0]["Problem"])
            question = problem_template.replace("{object}", object_item)
            print(idx, ": ", question)
            print()

            getting_answer(question, history, results, dataset, object_item)
            print('================= NEXT OBJECT =================')
            

    elif dataset == "Scientific_Test":
        for example in tqdm(data['Task']):
            for question in example['Example']:
                idx += 1
                print(idx, ": ", question)
                print()
                getting_answer(question, history, results, dataset, object_item=None)
                
            print(results)
            print()
    
    elif dataset == 'Instances_Test' or dataset == 'Similarities_Test':
        for question in tqdm(data['Examples']):
            idx += 1
            print(idx, ": ", question)
            print()

            getting_answer(question, history, results, dataset, object_item=None)

    else:
        print('ERROR!!!')

    write_output_file(history, 'history')
    write_output_file(results, 'answer')
    
# usage: python3 single_agent.py -d Scientific_Test -n 10