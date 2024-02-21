
from openai import OpenAI
import re
import os
import json
import datetime
from tqdm import tqdm

client = OpenAI()

input_file_name = "datasets/aut_30.json"
# input_file_name = "datasets/test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
output_file_name = f"reproduce_result/originality/AUT_reproduce_originality_{current_date}{formatted_time}.json"

yes = 0 
no = 0
other = 0

def call_openai_api(prompt):
    try:
        completion =  e(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        logprobs=True,
        top_logprobs=5
        )
        return completion.choices[0]
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def extract_purposes(text):
    lines = text.split('\n')
    cleaned_entries = [re.sub(r'^\d+\.\s*', '', line.strip()) for line in lines if line.strip()]
    return cleaned_entries

def parse(string, target):
    pattern = r"\b" + re.escape(target) + r"\b"
    return bool(re.search(pattern, string, re.IGNORECASE))

# def search_yes_no(logprobs_data):
    probabilities = {}
    search_tokens = ['Yes', 'No']
    for token_logprob in logprobs_data.content:
        for top_logprob in token_logprob.top_logprobs:
            if top_logprob.token in search_tokens:
                probabilities[top_logprob.token] = top_logprob.logprob
    return probabilities

if __name__ == "__main__":
    with open(input_file_name, "r") as file:
        data = json.load(file)

    item_uses_dict = {}

    for example in tqdm(data["examples"], desc='Handling Objects'):
        object = example["object"]
        question = f"What are some creative uses for {object}? The goal is to come up with creative ideas, which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different. List 10 creative uses for {object}."
        response = call_openai_api(question).message.content.strip()
        purposes = extract_purposes(response)

        if object not in item_uses_dict:
            item_uses_dict[object] = []

        for purpose in purposes:
            evaluation_prompt = f"If someone suggested using a {object} for the following purpose: {purpose}, would you be surprised and think it was a novel idea? Answer Yes or No."
            final_completion = call_openai_api(evaluation_prompt)
            final_answer = final_completion.message.content.strip()
            final_ans_prob = final_completion.logprobs
            # probabilities = search_yes_no(final_ans_prob)

            append_type = "Other"
            if parse(final_answer, "yes") and not parse(final_answer, "no"):
                append_type = "Yes"
                yes += 1
            elif parse(final_answer, "no") and not parse(final_answer, "yes"):
                append_type = "No"
                no += 1
            else:
                other += 1

            item_uses_dict[object].append({"use": purpose})

    results = [{"item": item, "uses": [use_info["use"] for use_info in uses]} for item, uses in item_uses_dict.items()]
    print(len(results))
    print('============================================')

    print(f"Yes = {yes}, No = {no}, Other = {other}.")
    with open(output_file_name, "w") as outfile:
        json.dump(results, outfile, indent=4)
    print('output file at: ', output_file_name)
