from openai import OpenAI
import re
import os

client = OpenAI()
import json
import datetime

agent = 1

input_file_name = "../../datasets/dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
output_file_name = f"../../results/reproduce/originality_result/AUT_reproduce_originality_{current_date}{formatted_time}.json"

yes = 0 
no = 0
other = 0

def call_openai_api(prompt):
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        logprobs = True,
        top_logprobs = 5
        )
        # print(completion.choices[0].logprobs)
        # return completion.choices[0].message.content.strip()
        return completion.choices[0]
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def extract_purposes(text):
    # Split the text by newlines
    lines = text.split('\n')
    cleaned_entries = []
    for line in lines:
        # Use regular expression to remove the number-dot prefix if it exists
        cleaned_entry = re.sub(r'^\d+\.\s*', '', line.strip())
        if cleaned_entry:  # To ensure not to add empty strings
            cleaned_entries.append(cleaned_entry)

    return cleaned_entries

    

def parse(string, target):
    # Pattern to match whole word, case insensitive
    pattern = r"\b" + re.escape(target) + r"\b"
    if re.search(pattern, string, re.IGNORECASE):
        return True
    else:
        return False

def search_yes_no(logprobs_data):
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

    results = []
    for example in data["examples"]:
        object = example["object"]
        question = f"What are some creative uses for {object}? The goal is to come up with creative ideas, which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different. List 10 creative uses for {object}."
        init_prompt = question
        response = call_openai_api(init_prompt).message.content.strip()
        print(f"RESPONSE: \n", response)
        purposes = extract_purposes(response)

        for purpose in purposes:

            #for Originality
            evaluation_prompt = f"If someone suggested using a {object} for the following purpose: {purpose}, would you be surprised and think it was a novel idea? Answer Yes or No."
            final_completion = call_openai_api(evaluation_prompt)
            final_answer = final_completion.message.content.strip()
            final_ans_prob = final_completion.logprobs
            probabilities = search_yes_no(final_ans_prob)

            append_type = ""
            yes_exist = parse(final_answer, "yes")
            no_exist = parse(final_answer, "no")

            if yes_exist == no_exist:
                print("APPEND_OTHER")
                append_type = "Other"
                other +=1
            elif yes_exist:
                print("APPEND_YES")
                append_type = "Yes"
                yes +=1
            elif no_exist:
                print("APPEND_N0")
                append_type = "No"
                no +=1
            else:
                print("APPEND_OTHER")
                append_type = "Other"
                other +=1
            result = {"item": object, "uses": purpose, "type": append_type, "full explanation": final_answer, "probabilities": probabilities}
            results.append(result)
            
    print(f"Yes = {yes}, No = {no}, Other = {other}.")
    with open(output_file_name, "w") as outfile:
        json.dump(results, outfile, indent=4)
