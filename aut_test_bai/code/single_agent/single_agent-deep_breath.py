import os
import re
import json
import datetime
from tqdm import tqdm
from openai import OpenAI

client = OpenAI()

agent = 1
input_file_name = "../../datasets/aut_10-1.json"

def write_output_file(results):
    folder_path = f"../../results/single_agent/"
    base_file_name = 'AUT_single_deep_breath_result'
    file_extension = '.json'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

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


if __name__ == "__main__":
    with open(input_file_name, "r") as file:
        data = json.load(file)

    results = []

    for example in tqdm(data["Examples"], desc="Processing Examples"):
        object_item = example["object"]
        problem_template = " ".join(data["Task"][0]["Problem"])
        question = problem_template.replace("{object}", object_item)
        question += " Take a Deep Breath."
        print(question)
        print()

        # initial_prompt = f"Initiate a discussion with others to collectively complete the following task: {question}"
        system_prompt = {"role": "system", "content": question}
        user_prompt = {"role": "user", "content": question}
        answer_context = [system_prompt, user_prompt]

        completion = generate_answer(answer_context)
        assistant_message = construct_assistant_message(completion)
        uses = extract_uses(assistant_message["content"])

        results.append({
            "item": object_item,
            "uses": uses,
        })
        print('================= NEXT OBJECT =================')
    
    write_output_file(results)
