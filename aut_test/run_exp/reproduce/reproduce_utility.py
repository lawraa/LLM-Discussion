from openai import OpenAI
import re
import os

client = OpenAI()
import json
import datetime

agent = 1
# input_file_name = "datasets/aut_100.json"
input_file_name = "../../datasets/dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
output_file_name = f"../../results/reproduce/utility_result/AUT_reproduce_utility_{current_date}{formatted_time}.json"

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

        return completion.choices[0]
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def extract_purposes(response):
    # Assuming each purpose is on a new line and starts with a number and a dot '1.', '2.', etc.
    lines = response.split('\n')
    purposes = []

    for line in lines:
        # Check if the line starts with a number and a dot, indicating it's one of the items
        if line.strip() and line[0].isdigit() and line[1] == '.':
            # Extract everything after 'number.' and strip whitespaces
            purpose = line.split('.', 1)[1].strip()
            purposes.append(purpose)

    return purposes

def parse(string, target):
    # Pattern to match whole word, case insensitive
    pattern = r"\b" + re.escape(target) + r"\b"
    if re.search(pattern, string, re.IGNORECASE):
        return True
    else:
        return False



def search_yes_no(logprobs_data):
    search_tokens = ['Yes', 'No']
    for token_logprob in logprobs_data.content:
        for top_logprob in token_logprob.top_logprobs:
            if top_logprob.token in search_tokens:
                print(f"Probability of '{top_logprob.token}': {top_logprob.logprob}")
            else:
                print("none.")
    return None

if __name__ == "__main__":
    with open(input_file_name, "r") as file:
        data = json.load(file)

    results = []
    for example in data["examples"]:
        #round_1
        object = example["object"]
        question = f"What are some creative uses for {object}? The goal is to come up with creative ideas, which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different.List 10 creative uses for {object}."
        input_prompt = question
        # print("INPUT: ", input_prompt)
        response = call_openai_api(input_prompt).message.content.strip()
        print(f"RESPONSE: \n", response)
        purposes = extract_purposes(response)

        for purpose in purposes:
            #round_2
            advantage_prompt = f"Q: Name one or more advantages to using a {object} for the following purpose: {purpose}?"
            # print("INPUT: ", advantage_prompt)
            advantages = call_openai_api(advantage_prompt).message.content.strip()
            print(f"ADVANTAGES: \n", advantages)

            #round_3
            drawback_prompt = f"Q: Name one or more drawbacks to using a {object} for the following purpose: {purpose}?"
            # print("INPUT: ", advantage_prompt)
            drawbacks = call_openai_api(drawback_prompt).message.content.strip()
            print(f"DRAWBACKS: \n",drawbacks)

            #round_4
            #for utility
            evaluation_prompt = f"Advantages:{advantages}\nDrawbacks: {drawbacks}\nQ: Based on these advantages and drawbacks, do you think using a {object} for the purpose {purpose}is a good idea? Answer Yes or No."
            print("INPUT: ", evaluation_prompt)
            # final_answer = call_openai_api(evaluation_prompt)
            final_completion = call_openai_api(evaluation_prompt)
            final_answer = final_completion.message.content.strip()
            # if final_answer.startswith("Yes") or final_answer.startswith("No"):
            final_ans_prob = final_completion.logprobs
            print(f"final_ans_prob = {final_ans_prob}")
            search_yes_no(final_ans_prob)
            # else:
            #     print("invalid final answer.")
            
            print("FINAL ANSWER: ",final_answer)

            
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

            results.append({"item": object, "uses": purpose,"adventages": advantages, "drawbacks": drawbacks ,"type": append_type, "full explanation": final_answer})
            print("------------------------------------------")
            
    print(f"Yes = {yes}, No = {no}, Other = {other}.")
    with open(output_file_name, "w") as outfile:
        json.dump(results, outfile, indent=4)
