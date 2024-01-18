import openai
import json
import datetime
from openai import OpenAI

agent = 1
input_file_name = "dataset_aut_test.json"
current_date = datetime.date.today().strftime("%m-%d_")
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
output_file_name = f"AUT_single_result_{agent}_{current_date}{formatted_time}.json"

client = OpenAI()
#print("MODELS: ", client.models.list())

def call_openai_api(prompt):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200,
            temperature=1,
            logprobs=10
        )
        # print("----------PROB = ")
        # print(response.choices[0].logprobs)

        return response.choices[0]
    except Exception as e:
        print(f"Error in API call: {e}")
        return None


def search_yes_no(logprobs_data):
    # Desired tokens to search for
    search_tokens = ['No', 'Yes']
    # Extracting and printing probabilities
    for top_logprobs in logprobs_data.top_logprobs:
        for token in search_tokens:
            prob = top_logprobs.get(token)
            if prob is not None:
                print(f"Probability of '{token}': {prob}")
            else:
                print("none.")
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


if __name__ == "__main__":
    with open(input_file_name, "r") as file:
        data = json.load(file)

    results = []
    for example in data["examples"]:
        #round_1
        object = example["input"]
        question = f"What are some creative uses for {object}? The goal is to come up with creative ideas, which are ideas that strike people as clever, unusual, interesting, uncommon, humorous, innovative, or different.List 10 creative uses for {object}."
        input_prompt = question
        # print("INPUT: ", input_prompt)
        response = call_openai_api(input_prompt).text
        print(f"RESPONSE: \n", response)
        purposes = extract_purposes(response)

        for purpose in purposes:
            #round_2
            advantage_prompt = f"Q: Name one or more advantages to using a {object} for the following purpose: {purpose}?"
            # print("INPUT: ", advantage_prompt)
            advantages = call_openai_api(advantage_prompt).text
            print(f"ADVANTAGES: \n", advantages)

            #round_3
            drawback_prompt = f"Q: Name one or more drawbacks to using a {object} for the following purpose: {purpose}?"
            # print("INPUT: ", advantage_prompt)
            drawbacks = call_openai_api(drawback_prompt).text
            print(f"DRAWBACKS: \n",drawbacks)

            #round_4
            evaluation_prompt = f"Advantages:{advantages}\nDrawbacks: {drawbacks}\nQ: Based on these advantages and drawbacks, do you think using a {object} for the purpose {purpose}is a good idea? Answer Yes or No."
            print("INPUT: ", evaluation_prompt)
            final_completion = call_openai_api(evaluation_prompt)
            # final_answer = final_completion.text
            final_answer = final_completion.text.strip()
            if final_answer.startswith("Yes") or final_answer.startswith("No"):
                final_ans_prob = final_completion.logprobs
                search_yes_no(final_ans_prob)
            print("FINAL ANSWER: ",final_answer)
            print("------------------------------------------")


            #print
            results.append({"init": input_prompt, "model_response_1": response, "input_2": advantage_prompt, "advantages": advantages, "input_3": drawback_prompt, "drawbacks": drawbacks, "input_4": evaluation_prompt, "final_ans": final_answer })
            # print({"input": input_prompt, "model_response": response, "target": example["target"]})
    
    with open(output_file_name, "w") as outfile:
        json.dump(results, outfile, indent=4)
